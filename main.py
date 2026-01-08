import asyncio
import json
from workflows.builder import WorkflowBuilder


def main():
    with open("test_workflow.json") as f:
        raw_workflow = json.load(f)

    builder = WorkflowBuilder(raw_workflow)
    workflow = builder.build()

    state = {}
    variables = {"age": 25, "name": "John"}

    print(f"Executing workflow: {workflow.name}")
    print("--- First Run ---")
    print(f"Initial state: {state}")
    print(f"Initial variables: {variables}")
    print("-" * 40)

    asyncio.run(workflow.execute_async(state, variables))

    print("-" * 40)
    print(f"Final state: {state}")
    print("--- End of First Run ---")

    print("\n\n--- Second Run with Different Variables ---")
    state = {}
    variables = {"age": 17, "name": "Alice"}
    print(f"Initial state: {state}")
    print(f"Initial variables: {variables}")
    print("-" * 40)
    asyncio.run(workflow.execute_async(state, variables))
    print("-" * 40)
    print(f"Final state: {state}")
    print("--- End of Second Run ---")


if __name__ == "__main__":
    main()
