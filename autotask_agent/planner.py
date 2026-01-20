import json
import base64
import mimetypes
from anthropic import Anthropic
from loguru import logger
from typing import Dict, List, Optional


ALLOWED_ACTIONS = {
    "tap",
    "swipe",
    "input_text",
    "open_app",
    "press_back",
    "press_home",
    "find_and_tap",
    "scroll",
    "wait",
}


class TaskPlanner:
    """AI-powered Android task planner with safety constraints"""

    def __init__(self, client: Anthropic):
        self.client = client


    def _encode_image(self, path: str) -> Dict:
        mime, _ = mimetypes.guess_type(path)
        mime = mime or "image/png"

        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")

        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mime,
                "data": data,
            },
        }

    def _sanitize_plan(self, plan: Dict) -> Dict:
        """Validate and clean AI-generated plan"""

        steps = []
        for step in plan.get("steps", []):
            action = step.get("action_type")

            if action not in ALLOWED_ACTIONS:
                logger.warning(f"Dropping invalid action: {action}")
                continue

            steps.append({
                "step_number": step.get("step_number", len(steps) + 1),
                "description": step.get("description", ""),
                "action_type": action,
                "params": step.get("params", {}),
                "reason": step.get("reason", ""),
            })

        if not steps:
            logger.error("Planner returned empty/invalid plan")
            steps = [{
                "step_number": 1,
                "description": "Wait safely",
                "action_type": "wait",
                "params": {"seconds": 1},
                "reason": "Fallback safe step",
            }]

        plan["steps"] = steps
        return plan


    def create_plan(self, task: str, screenshot_path: Optional[str] = None) -> Dict:
        """Create a safe execution plan"""

        content = []

        if screenshot_path:
            content.append(self._encode_image(screenshot_path))

        content.append({
            "type": "text",
            "text": f"""
You are an Android automation planner.

Rules:
- Prefer semantic actions like find_and_tap over coordinates
- Use tap/swipe coordinates ONLY if unavoidable
- Use ONLY these action types:
  {", ".join(ALLOWED_ACTIONS)}
- Assume app may NOT be open
- Do NOT hallucinate package names

TASK:
{task}

Respond ONLY with valid JSON:

{{
  "steps": [
    {{
      "step_number": 1,
      "description": "...",
      "action_type": "open_app",
      "params": {{}},
      "reason": "..."
    }}
  ],
  "estimated_time": "...",
  "complexity": "low | medium | high"
}}
"""
        })

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": content}],
            )

            text = response.content[0].text.strip()

            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()

            plan = json.loads(text)
            plan = self._sanitize_plan(plan)

            logger.info(f"Plan created: {len(plan['steps'])} steps")
            return plan

        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return {
                "steps": [{
                    "step_number": 1,
                    "description": "Wait",
                    "action_type": "wait",
                    "params": {"seconds": 1},
                    "reason": "Planner error fallback",
                }],
                "estimated_time": "unknown",
                "complexity": "high",
                "error": str(e),
            }


    def analyze_failure(self, failed_step: Dict, screenshot_path: str) -> Optional[Dict]:
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": [
                        self._encode_image(screenshot_path),
                        {
                            "type": "text",
                            "text": f"""
This automation step failed:
{json.dumps(failed_step, indent=2)}

Explain why and suggest ONE alternative safe action.
Respond ONLY in JSON.
"""
                        },
                    ],
                }],
            )

            text = response.content[0].text
            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()

            return json.loads(text)

        except Exception as e:
            logger.error(f"Failure analysis failed: {e}")
            return None


    def optimize_plan(self, plan: Dict, execution_results: List[Dict]) -> Dict:
        failures = [r for r in execution_results if not r.get("success")]

        if not failures:
            return plan

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{
                    "role": "user",
                    "content": f"""
Original plan:
{json.dumps(plan, indent=2)}

Failures:
{json.dumps(failures, indent=2)}

Generate an improved plan using ONLY allowed actions.
Return full JSON.
"""
                }],
            )

            text = response.content[0].text
            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()

            improved = json.loads(text)
            return self._sanitize_plan(improved)

        except Exception as e:
            logger.error(f"Plan optimization failed: {e}")
            return plan