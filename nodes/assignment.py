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
        connections: list[NodeConnection] | None = None,
        parameters: dict | None = None,
    ):
        super().__init__(name, description, parameters or {}, connections or [])

        self.variable_name = variable
        self.value = value

    async def execute_async(self, state: dict, variables: dict, **kwargs):
        # Implement the asynchronous execution logic for setting a variable
        # Try to extract from combined state/variables, fallback to literal value
        combined_data = {**state, **variables}
        extracted_value = get_var(combined_data, self.value, self.value)
        state[self.variable_name] = extracted_value

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "variable_name": self.variable_name,
            "value": self.value,
        }
