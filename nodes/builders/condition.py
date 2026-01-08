from collections.abc import Generator
from nodes.builders.base import NodeBuilder
from nodes.condition import ConditionNode


class ConditionNodeBuilder(NodeBuilder[ConditionNode]):
    def create(self) -> ConditionNode:
        return ConditionNode(
            name=self.name,
            description=self.description,
            condition=self.parameters.get("condition", {}),
            parameters=self.parameters,
        )

    def get_errors(self) -> Generator[str, None, None]:
        if "condition" not in self.parameters:
            yield "Missing 'condition' parameter"

        return
