from typing import TYPE_CHECKING

from nodes.base import BaseNode
from nodes.connection import ConnectionLabel, NodeConnection

if TYPE_CHECKING:
    from workflows.context import ExecutionContext


class ForLoopNode(BaseNode):
    name: str
    description: str
    type: str = "for"

    # Keys for node_context storage
    LOOP_INDEX_KEY = "__index"
    LOOP_COLLECTION_KEY = "__collection"
    ITEM_KEY = "item"
    INDEX_KEY = "index"

    def __init__(
        self,
        name: str,
        description: str,
        collection: str,
        iterator_var: str | None = None,
        index_var: str | None = None,
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

        self.collection = collection
        self.iterator_var = iterator_var  # Optional: also store in state for backward compat
        self.index_var = index_var  # Optional: also store in state for backward compat
        self.body_node: BaseNode | None = None
        self.exit_node: BaseNode | None = None

        self.link(connections or [])

    def link(self, connections: list[NodeConnection]):
        super().link(connections)

        self.body_node = next(
            (conn.to for conn in self.connections if conn.label == ConnectionLabel.BODY),
            None,
        )
        self.exit_node = next(
            (conn.to for conn in self.connections if conn.label == ConnectionLabel.EXIT),
            None,
        )

    async def execute_async(self, ctx: "ExecutionContext") -> None:
        node_ctx = ctx.get_node_context(self.name)

        # Initialize loop state on first call
        if self.LOOP_INDEX_KEY not in node_ctx:
            # Get collection from context path
            collection = ctx.get(self.collection, None)

            # If not found, try as literal
            if collection is None:
                collection = []

            if not isinstance(collection, (list, tuple)):
                collection = []

            ctx.set_node_context(
                self.name,
                {
                    self.LOOP_INDEX_KEY: 0,
                    self.LOOP_COLLECTION_KEY: list(collection),
                },
            )
            node_ctx = ctx.get_node_context(self.name)

        # Set current item and index in node_context
        index = node_ctx[self.LOOP_INDEX_KEY]
        collection = node_ctx[self.LOOP_COLLECTION_KEY]

        if index < len(collection):
            ctx.update_node_context(self.name, self.ITEM_KEY, collection[index])
            ctx.update_node_context(self.name, self.INDEX_KEY, index)

            # Backward compatibility: also set in state if iterator_var/index_var specified
            if self.iterator_var:
                ctx.set(self.iterator_var, collection[index])
            if self.index_var:
                ctx.set(self.index_var, index)

    async def next_nodes(self, ctx: "ExecutionContext") -> list[BaseNode]:
        node_ctx = ctx.get_node_context(self.name)

        if not node_ctx or self.LOOP_INDEX_KEY not in node_ctx:
            # No loop state, exit
            return [self.exit_node] if self.exit_node else []

        index = node_ctx[self.LOOP_INDEX_KEY]
        collection = node_ctx[self.LOOP_COLLECTION_KEY]

        if index < len(collection):
            # More items to iterate
            return [self.body_node] if self.body_node else []
        else:
            # Loop complete, clean up and exit
            ctx.clear_node_context(self.name)
            return [self.exit_node] if self.exit_node else []

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "collection": self.collection,
            "iterator_var": self.iterator_var,
            "index_var": self.index_var,
        }


class EndLoopNode(BaseNode):
    name: str
    description: str
    type: str = "end_loop"

    def __init__(
        self,
        name: str,
        description: str,
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

    async def execute_async(self, ctx: "ExecutionContext") -> None:
        # Find the loop node from connections and increment its counter
        for conn in self.connections:
            if isinstance(conn.to, ForLoopNode):
                node_ctx = ctx.get_node_context(conn.to.name)
                if node_ctx and ForLoopNode.LOOP_INDEX_KEY in node_ctx:
                    node_ctx[ForLoopNode.LOOP_INDEX_KEY] += 1
                break

    async def next_nodes(self, ctx: "ExecutionContext") -> list[BaseNode]:
        return [conn.to for conn in self.connections if conn.to]

    def to_dict(self) -> dict:
        return super().to_dict()
