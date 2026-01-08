import argparse
import asyncio
import json
from workflows.builder import WorkflowBuilder


def main():
    parser = argparse.ArgumentParser(description="Run a workflow from a JSON file")
    parser.add_argument("workflow_file", help="Path to the workflow JSON file")
    parser.add_argument(
        "--var",
        "-v",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Initial variable (can be used multiple times)",
    )
    args = parser.parse_args()

    with open(args.workflow_file) as f:
        raw_workflow = json.load(f)

    builder = WorkflowBuilder(raw_workflow)
    workflow = builder.build()

    state = {}
    variables = {}
    if args.var:
        for key, value in args.var:
            # Try to parse as JSON, fallback to string
            try:
                variables[key] = json.loads(value)
            except json.JSONDecodeError:
                variables[key] = value

    print(f"Executing workflow: {workflow.name}")
    print(f"Initial state: {state}")
    print(f"Initial variables: {variables}")
    print("-" * 40)

    asyncio.run(workflow.execute_async(state, variables))

    print("-" * 40)
    print(f"Final state: {state}")


if __name__ == "__main__":
    main()
