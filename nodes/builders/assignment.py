from collections.abc import Generator
from nodes.assignment import SetNode
from nodes.builders.base import NodeBuilder


class SetNodeBuilder(NodeBuilder[SetNode]):
    def create(self) -> SetNode:
        return SetNode(
            name=self.name,
            description=self.description,
            variable=self.parameters.get("variable_name", ""),
            value=self.parameters.get("value", ""),
            parameters=self.parameters,
        )

    def get_errors(self) -> Generator[str, None, None]:
        if "variable_name" not in self.parameters:
            yield "Missing 'variable_name' parameter"
        if "value" not in self.parameters:
            yield "Missing 'value' parameter"

        return
