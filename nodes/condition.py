from typing import TYPE_CHECKING

from json_logic import jsonLogic

from nodes.base import BaseNode
from nodes.connection import ConnectionLabel, NodeConnection

if TYPE_CHECKING:
    from workflows.context import ExecutionContext


class ConditionNode(BaseNode):
    name: str
    description: str
    type: str = "if"

    def __init__(
        self,
        name,
        description,
        condition: dict,  # json logic condition
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

        self.condition = condition
        self.link(connections or [])

    def link(self, connections):
        super().link(connections)

        self.true_node = next(
            (conn.to for conn in self.connections if conn.label == ConnectionLabel.TRUE),
            None,
        )
        self.false_node = next(
            (conn.to for conn in self.connections if conn.label == ConnectionLabel.FALSE),
            None,
        )

    async def execute_async(self, ctx: "ExecutionContext") -> None:
        # ConditionNode only determines next nodes, doesn't execute logic
        pass

    async def next_nodes(self, ctx: "ExecutionContext") -> list["BaseNode"]:
        # Combine state and node_context for condition evaluation
        data = {**ctx.state, **ctx.node_context}
        result = jsonLogic(self.condition, data)
        if result:
            return [self.true_node] if self.true_node else []

        return [self.false_node] if self.false_node else []

    def to_dict(self) -> dict:
        return {**super().to_dict(), "condition": self.condition}
