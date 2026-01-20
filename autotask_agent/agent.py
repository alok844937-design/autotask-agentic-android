import os
from loguru import logger

class AutoTaskAgent:
    def __init__(self):
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

        if self.mock_mode:
            logger.warning("MOCK MODE ENABLED — skipping Android device connection")
            self.device = None
            self.client = None
            return

        # Real mode (not used in demo)
        from .actions import AndroidActions
        self.device = AndroidActions()

    def execute_task(self, task: str):
        """
        Execute a natural language task on Android.
        In MOCK MODE, actions are simulated.
        """

        logger.info(f"Received task: {task}")

        # -------- MOCK MODE --------
        if self.mock_mode:
            plan = [
                "Open Settings app",
                "Navigate to Network & Internet",
                "Toggle WiFi ON"
            ]

            print("\nAgent Plan:")
            for step in plan:
                print(f"- {step}")

            print("\nExecuting actions (simulated)...")
            for step in plan:
                print(f"✓ {step}")

            result = {
                "success": True,
                "mode": "mock",
                "task": task,
                "steps_executed": plan
            }

            print("\nExecution Result:")
            print(result)

            return result

        # -------- REAL MODE (future) --------
        raise NotImplementedError("Real device execution not enabled yet")