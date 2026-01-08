# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based workflow builder that enables defining, constructing, and executing workflows composed of connected nodes. Uses async execution patterns and builder pattern for workflow construction.

## Commands

```bash
# Install dependencies
uv sync

# Run the project
uv run python main.py

# Run a specific Python file
uv run python <file.py>
```

## Architecture

### Core Concepts

**Workflow Execution Flow:**
1. JSON workflow definition → `WorkflowBuilder` parses raw data
2. `NodeFactory` creates typed nodes via builders (validates parameters)
3. `ConnectionBuilder` links nodes by name with labeled edges
4. `Workflow.execute_async()` runs nodes starting from entry points (no incoming connections)

### Key Patterns

- **Builder Pattern**: All nodes created through builders (`SetNodeBuilder`, `ConditionNodeBuilder`) that validate before instantiation
- **Factory Pattern**: `NodeFactory.create_node(type, name, description, parameters)` maps type strings to builders
- **Async-First**: All node execution via `execute_async(state, variables)` with parallel execution at each level

### Node System

**BaseNode** (`nodes/base.py`): Abstract base with `execute_async()`, `next_nodes()`, `set_connections()`

**Node Types:**
- `"set"` → `SetNode`: Variable assignment via `variable_name` and `value` parameters
- `"if"` → `ConditionNode`: Conditional branching using JSON Logic; uses "true"/"false" labeled connections

**Connections**: `NodeConnection(to, label)` where label defaults to "main", condition nodes use "true"/"false"

### State Management

- `state`: Shared mutable dict passed through execution
- `variables`: Copied per execution level for isolation
- Variable extraction supports dot notation (`user.profile.age`) and array indexing (`items.0.name`) via `utils/extract.py`

### Type Definitions

Raw data structures use `TypedDict`:
- `RawNode`: name, description, position, type, parameters
- `RawConnection`: to (node name), label
- `RawWorkflow`: name, nodes, connections

## Adding New Node Types

1. Create node class in `nodes/` extending `BaseNode`
2. Create builder in `nodes/builders/` extending `NodeBuilder[YourNode]`
3. Register in `NodeFactory.get_builder()` with type string mapping

## Dependencies

- `json-logic`: Evaluates conditional expressions in `ConditionNode`
