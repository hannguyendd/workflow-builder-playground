from nodes.base import BaseNode
from nodes.connection import NodeConnection
from json_logic import jsonLogic


class ConditionNode(BaseNode):
    name: str
    description: str
    type: str = "if"

    def __init__(
        self,
        name,
        description,
        condition: dict,  # json logic condition
        connections=list[NodeConnection],
        parameters={},
    ):
        super().__init__(name, description, parameters, connections)

        self.condition = condition
        self.set_connections(connections)

    def set_connections(self, connections):
        super().set_connections(connections)

        self.true_node = next(
            (conn.to for conn in self.connections if conn.label == "true"), None
        )
        self.false_node = next(
            (conn.to for conn in self.connections if conn.label == "false"), None
        )

    async def execute_async(self, state: dict, variables: dict, **kwargs):
        # Implement the asynchronous execution logic f  or the condition node
        pass

    async def next_nodes(self, state, variables):
        data = {state, variables}
        result = jsonLogic(self.condition, data)
        if result:
            return [self.true_node] if self.true_node else []

        return [self.false_node] if self.false_node else []

    def to_dict(self) -> dict:
        # Implement serialization logic specific to ConditionNode
        return {**super().to_dict(), "condition": self.condition}
