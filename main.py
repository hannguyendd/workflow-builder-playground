import argparse
import asyncio
import json

from workflows.builder import WorkflowBuilder
from workflows.context import ExecutionContext


def main():
    parser = argparse.ArgumentParser(description="Run a workflow from a JSON file")
    parser.add_argument("workflow_file", help="Path to the workflow JSON file")
    parser.add_argument(
        "--var",
        "-v",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Initial state variable (can be used multiple times)",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="Path to config JSON file",
    )
    args = parser.parse_args()

    with open(args.workflow_file) as f:
        raw_workflow = json.load(f)

    builder = WorkflowBuilder(raw_workflow)
    workflow = builder.build()

    state = {}
    if args.var:
        for key, value in args.var:
            # Try to parse as JSON, fallback to string
            try:
                state[key] = json.loads(value)
            except json.JSONDecodeError:
                state[key] = value

    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    ctx = ExecutionContext(state=state, config=config)

    print(f"Executing workflow: {workflow.name}")
    print(f"Initial state: {ctx.state}")
    print(f"Config: {ctx.config}")
    print("-" * 40)

    asyncio.run(workflow.execute_async(ctx))

    print("-" * 40)
    print(f"Final state: {ctx.state}")
    print(f"Node context: {ctx.node_context}")


if __name__ == "__main__":
    main()
