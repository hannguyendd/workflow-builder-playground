from collections.abc import Generator
from nodes.builders.base import NodeBuilder
from nodes.loop import ForLoopNode, EndLoopNode


class ForLoopNodeBuilder(NodeBuilder[ForLoopNode]):
    def create(self) -> ForLoopNode:
        return ForLoopNode(
            name=self.name,
            description=self.description,
            collection=self.parameters.get("collection", ""),
            iterator_var=self.parameters.get("iterator_var", ""),
            index_var=self.parameters.get("index_var"),
            parameters=self.parameters,
        )

    def get_errors(self) -> Generator[str, None, None]:
        if "collection" not in self.parameters:
            yield "Missing 'collection' parameter"
        # iterator_var is optional - nodes can access via node_context (e.g., "loop_node.item")


class EndLoopNodeBuilder(NodeBuilder[EndLoopNode]):
    def create(self) -> EndLoopNode:
        return EndLoopNode(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    def get_errors(self) -> Generator[str, None, None]:
        yield from ()
