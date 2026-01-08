from collections.abc import Generator
from nodes.builders.base import NodeBuilder
from nodes.condition import ConditionNode


class ConditionNodeBuilder(NodeBuilder[ConditionNode]):
    def build(self) -> ConditionNode:
        return ConditionNode(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    def get_errors(self) -> Generator[str, None, None]:
        if "condition" not in self.parameters:
            yield "Missing 'condition' parameter"

        return
