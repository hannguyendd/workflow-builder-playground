from typing import TYPE_CHECKING

from nodes.base import BaseNode
from nodes.connection import NodeConnection

if TYPE_CHECKING:
    from workflows.context import ExecutionContext


class SetNode(BaseNode):
    name: str
    description: str
    type: str = "set"

    def __init__(
        self,
        name,
        description,
        variable: str,
        value: str,
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

        self.variable_name = variable
        self.value = value

    async def execute_async(self, ctx: "ExecutionContext") -> None:
        # Try to extract from context, fallback to literal value
        extracted_value = ctx.get(self.value, self.value)
        ctx.set(self.variable_name, extracted_value)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "variable_name": self.variable_name,
            "value": self.value,
        }
