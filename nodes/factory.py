from nodes.base import BaseNode


class NodeFactory:
    def get_builder(self, node_type: str):
        if node_type == "set":
            from nodes.builders.assignment import SetNodeBuilder

            return SetNodeBuilder
        elif node_type == "if":
            from nodes.builders.condition import ConditionNodeBuilder

            return ConditionNodeBuilder
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def create_node(
        self, node_type: str, name: str, description: str, parameters: dict
    ) -> BaseNode:
        builder_type = self.get_builder(node_type)
        node_builder = builder_type(
            name=name, description=description, parameters=parameters
        )

        return node_builder.build()
