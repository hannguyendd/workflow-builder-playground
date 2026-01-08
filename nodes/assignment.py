from nodes.base import BaseNode
from nodes.connection import NodeConnection
from utils.extract import get_var


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
        connections=list[NodeConnection],
        parameters={},
    ):
        super().__init__(name, description, parameters, connections)

        self.variable_name = variable
        self.value = value

    async def execute_async(self, state: dict, variables: dict, **kwargs):
        # Implement the asynchronous execution logic for setting a variable
        extracted_value = get_var(self.value, state, variables)
        state[self.variable_name] = extracted_value

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "variable_name": self.variable_name,
            "value": self.value,
        }
