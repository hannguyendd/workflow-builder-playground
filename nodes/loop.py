from nodes.base import BaseNode
from nodes.connection import NodeConnection
from utils.extract import get_var


class ForLoopNode(BaseNode):
    name: str
    description: str
    type: str = "for"

    def __init__(
        self,
        name: str,
        description: str,
        collection: str,
        iterator_var: str,
        index_var: str | None = None,
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

        self.collection = collection
        self.iterator_var = iterator_var
        self.index_var = index_var
        self.body_node: BaseNode | None = None
        self.exit_node: BaseNode | None = None

        self.set_connections(connections or [])

    def _get_loop_key(self) -> str:
        return f"__loop_{self.name}"

    def set_connections(self, connections: list[NodeConnection]):
        super().set_connections(connections)

        self.body_node = next(
            (conn.to for conn in self.connections if conn.label == "body"), None
        )
        self.exit_node = next(
            (conn.to for conn in self.connections if conn.label == "exit"), None
        )

    async def execute_async(self, state: dict, variables: dict, **kwargs):
        loop_key = self._get_loop_key()

        # Initialize loop state on first call
        if loop_key not in state:
            combined_data = {**state, **variables}
            collection = get_var(combined_data, self.collection, self.collection)

            # If collection is still a string, try to get it directly from combined_data
            if isinstance(collection, str):
                collection = combined_data.get(collection, [])

            if not isinstance(collection, (list, tuple)):
                collection = []

            state[loop_key] = {
                "index": 0,
                "collection": list(collection),
            }

        # Set iterator and index variables for current iteration
        # Store in state so they persist across levels (variables are copied per level)
        loop_state = state[loop_key]
        index = loop_state["index"]
        collection = loop_state["collection"]

        if index < len(collection):
            state[self.iterator_var] = collection[index]
            if self.index_var:
                state[self.index_var] = index

    async def next_nodes(self, state: dict, variables: dict) -> list[BaseNode]:
        loop_key = self._get_loop_key()
        loop_state = state.get(loop_key)

        if not loop_state:
            # No loop state, exit
            return [self.exit_node] if self.exit_node else []

        index = loop_state["index"]
        collection = loop_state["collection"]

        if index < len(collection):
            # More items to iterate
            return [self.body_node] if self.body_node else []
        else:
            # Loop complete, clean up and exit
            del state[loop_key]
            # Clean up iterator variables
            if self.iterator_var in state:
                del state[self.iterator_var]
            if self.index_var and self.index_var in state:
                del state[self.index_var]
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

    async def execute_async(self, state: dict, variables: dict, **kwargs):
        # Find the loop node from connections and increment its counter
        for conn in self.connections:
            if isinstance(conn.to, ForLoopNode):
                loop_key = conn.to._get_loop_key()
                if loop_key in state:
                    state[loop_key]["index"] += 1
                break

    async def next_nodes(self, state: dict, variables: dict) -> list[BaseNode]:
        return [conn.to for conn in self.connections if conn.to]

    def to_dict(self) -> dict:
        return super().to_dict()
