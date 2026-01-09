# Workflow Builder Playground

A Python-based workflow builder that enables defining, constructing, and executing workflows composed of connected nodes. Define workflows in JSON, and the engine handles async execution with parallel processing.

## Features

- **JSON-based workflow definitions** - Define workflows declaratively
- **Async execution** - Nodes at the same level execute in parallel
- **Multiple node types** - Variable assignment, conditionals, loops
- **Builder pattern** - Type-safe node construction with validation
- **Nested variable access** - Dot notation for deep object access (`user.profile.age`)

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd workflow-builder-playground

# Install dependencies
uv sync
```

## Usage

### Run a workflow

```bash
# Run the default workflow
uv run python main.py

# Run a specific workflow file
uv run python main.py examples/loop_workflow.json

# Run with initial variables
uv run python main.py examples/test_workflow.json -v '{"user": {"name": "Alice"}}'
```

## Workflow Structure

Workflows are defined in JSON with three main sections:

```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...}
}
```

### Nodes

Each node has:
- `name`: Unique identifier
- `description`: Human-readable description
- `position`: [x, y] coordinates (for visualization)
- `type`: Node type (`set`, `if`, `for`, `end_loop`)
- `parameters`: Type-specific parameters

### Connections

Map node names to arrays of connections:
```json
{
  "node_name": [
    {"to": "target_node", "label": "main"}
  ]
}
```

Connection labels:
- `main` - Default flow
- `true` / `false` - Conditional branches
- `body` / `exit` - Loop branches

## Node Types

### SetNode (`set`)

Assigns a value to a variable.

```json
{
  "type": "set",
  "parameters": {
    "variable_name": "status",
    "value": "active"
  }
}
```

### ConditionNode (`if`)

Branches based on a condition using [JSON Logic](https://jsonlogic.com/).

```json
{
  "type": "if",
  "parameters": {
    "condition": {
      ">=": [{"var": "age"}, 18]
    }
  }
}
```

### ForLoopNode (`for`)

Iterates over a collection.

```json
{
  "type": "for",
  "parameters": {
    "collection": "items",
    "iterator_var": "current_item",
    "index_var": "index"
  }
}
```

### EndLoopNode (`end_loop`)

Marks the end of a loop body, returning control to the loop node.

```json
{
  "type": "end_loop",
  "parameters": {}
}
```

## Examples

### Basic Conditional Workflow

```json
{
  "name": "Age Check Workflow",
  "nodes": [
    {
      "name": "set_age",
      "type": "set",
      "parameters": {"variable_name": "age", "value": 25}
    },
    {
      "name": "check_adult",
      "type": "if",
      "parameters": {"condition": {">=": [{"var": "age"}, 18]}}
    },
    {
      "name": "adult_branch",
      "type": "set",
      "parameters": {"variable_name": "status", "value": "adult"}
    },
    {
      "name": "minor_branch",
      "type": "set",
      "parameters": {"variable_name": "status", "value": "minor"}
    }
  ],
  "connections": {
    "set_age": [{"to": "check_adult", "label": "main"}],
    "check_adult": [
      {"to": "adult_branch", "label": "true"},
      {"to": "minor_branch", "label": "false"}
    ]
  }
}
```

### Loop Workflow

See `examples/loop_workflow.json` for a complete loop example.

## Project Structure

```
workflow-builder-playground/
├── nodes/              # Node implementations
│   ├── base.py         # BaseNode abstract class
│   ├── assignment.py   # SetNode
│   ├── condition.py    # ConditionNode
│   ├── loop.py         # ForLoopNode, EndLoopNode
│   ├── factory.py      # NodeFactory
│   └── builders/       # Node builders with validation
├── workflows/          # Workflow engine
│   ├── base.py         # Workflow class
│   └── builder.py      # WorkflowBuilder
├── utils/              # Utilities
│   └── extract.py      # Variable extraction helpers
├── examples/           # Example workflows
└── main.py             # CLI entry point
```

## License

MIT
