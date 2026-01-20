import os
from loguru import logger

def main():
    print("\n AutoTask Agentic Android - Hackathon Demo\n")
    
    os.environ["MOCK_MODE"] = "true"

    try:
        from autotask_agent.agent import AutoTaskAgent

        agent = AutoTaskAgent()

        if agent.mock_mode:
            print("Running in MOCK MODE - Android actions simulated\n")

        task = "Open settings and turn on WiFi"

        print(f"Task: {task}\n")
        result = agent.execute_task(task)

        print("\n Execution Result:")
        print(result)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print("\n Execution failed - check logs above\n")


if __name__ == "__main__":
    main()