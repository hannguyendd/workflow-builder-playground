from abc import abstractmethod
from typing import TypedDict

from nodes.connection import NodeConnection


class RawNode(TypedDict):
    name: str
    description: str
    position: tuple[int, int]
    type: str
    parameters: dict


class BaseNode:
    name: str
    description: str
    type: str
    parameters: dict
    connections: list[NodeConnection] = []

    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict = {},
        connections: list[NodeConnection] = [],
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.connections = connections

    def is_valid(self, parameters: dict) -> bool:
        return True

    @abstractmethod
    async def execute_async(self, state: dict, variables: dict, **kwargs):
        pass

    async def next_nodes(self, state: dict, variables: dict) -> list["BaseNode"]:
        return [conn.to for conn in self.connections]

    def set_connections(self, connections: list[NodeConnection]):
        self.connections = connections

    @abstractmethod
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
        }
