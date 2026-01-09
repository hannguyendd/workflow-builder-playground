# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python workflow builder for defining, constructing, and executing workflows composed of connected nodes. Uses async execution with parallel processing and builder pattern for type-safe node construction.

## Commands

```bash
# Install dependencies
uv sync

# Run the default workflow
uv run python main.py

# Run a specific workflow file
uv run python main.py examples/loop_workflow.json

# Run with initial variables
uv run python main.py examples/test_workflow.json -v '{"user": {"name": "Alice"}}'
```

## Architecture

### Execution Flow

1. JSON workflow definition → `WorkflowBuilder` parses raw data
2. `NodeFactory` creates typed nodes via builders (validates parameters)
3. `ConnectionBuilder` links nodes by name with labeled edges
4. `Workflow.execute_async()` runs nodes starting from entry points (no incoming connections)
5. Nodes at same level execute in parallel via `asyncio.gather()`

### Key Patterns

- **Builder Pattern**: All nodes created through builders that validate before instantiation
- **Factory Pattern**: `NodeFactory.create_node(type, name, description, parameters)` maps type strings to builders
- **Async-First**: All node execution via `execute_async(state, variables)` with parallel execution at each level

### Node System

**BaseNode** (`nodes/base.py`): Abstract base with `execute_async()`, `next_nodes()`, `set_connections()`

**Node Types:**
| Type | Class | File | Description |
|------|-------|------|-------------|
| `set` | `SetNode` | `nodes/assignment.py` | Variable assignment via `variable_name` and `value` parameters |
| `if` | `ConditionNode` | `nodes/condition.py` | Conditional branching using JSON Logic; uses "true"/"false" labeled connections |
| `for` | `ForLoopNode` | `nodes/loop.py` | Iteration with `collection`, `iterator_var`, and optional `index_var`; uses "body"/"exit" connections |
| `end_loop` | `EndLoopNode` | `nodes/loop.py` | Marks end of loop body, increments index, returns control to ForLoopNode |

**Connection Labels** (`nodes/connection.py`):
- `main`: Default flow (SetNode, general)
- `true` / `false`: ConditionNode branches
- `body` / `exit`: ForLoopNode branches

### State Management

- `state`: Shared mutable dict passed through execution, persists across all levels
- `variables`: Copied per execution level for isolation
- **Loop state**: ForLoopNode stores iteration state in `state["__loop_{node_name}"]` containing collection, current index
- Variable extraction supports dot notation (`user.profile.age`) and array indexing (`items.0.name`) via `utils/extract.py`

### Type Definitions

Raw data structures use `TypedDict`:
- `RawNode`: name, description, position, type, parameters
- `RawConnection`: to (node name), label
- `RawWorkflow`: name, nodes, connections

## File Structure

```
workflow-builder-playground/
├── nodes/                          # Node implementations
│   ├── base.py                     # BaseNode abstract class, RawNode TypedDict
│   ├── assignment.py               # SetNode
│   ├── condition.py                # ConditionNode
│   ├── loop.py                     # ForLoopNode, EndLoopNode
│   ├── connection.py               # NodeConnection, RawConnection
│   ├── factory.py                  # NodeFactory
│   ├── exceptions.py               # NodeException, NodeValidationException
│   └── builders/                   # Node builders
│       ├── base.py                 # NodeBuilder[T] generic base class
│       ├── assignment.py           # SetNodeBuilder
│       ├── condition.py            # ConditionNodeBuilder
│       ├── loop.py                 # ForLoopNodeBuilder, EndLoopNodeBuilder
│       └── connection.py           # ConnectionBuilder
├── workflows/                      # Workflow engine
│   ├── base.py                     # Workflow, RawWorkflow
│   ├── builder.py                  # WorkflowBuilder
│   └── exception.py                # CreateNodeException
├── utils/                          # Utilities
│   ├── extract.py                  # get_var() for nested variable extraction
│   └── expression.py               # Expression classes (not currently integrated)
├── examples/                       # Example workflows
│   ├── test_workflow.json          # Basic set/if nodes example
│   └── loop_workflow.json          # ForLoop/EndLoop example
└── main.py                         # CLI entry point
```

## Adding New Node Types

1. Create node class in `nodes/` extending `BaseNode`
2. Implement `execute_async(state, variables, **kwargs)` method
3. Override `next_nodes()` if custom routing needed (e.g., conditional branches)
4. Create builder in `nodes/builders/` extending `NodeBuilder[YourNode]`
5. Implement `get_errors()` generator for parameter validation
6. Register in `NodeFactory.get_builder()` with type string mapping

## Exception Handling

- `NodeException` (`nodes/exceptions.py`): Base exception for node-related errors
- `NodeValidationException` (`nodes/exceptions.py`): Raised during builder validation with `type`, `message`, `parameters`
- `CreateNodeException` (`workflows/exception.py`): Holds list of errors from workflow building

## Dependencies

- `json-logic-qubit` (>=0.9.1): Evaluates conditional expressions in ConditionNode
- Python >=3.12
