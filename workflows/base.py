import asyncio
from typing import TypedDict
from nodes.base import BaseNode, RawNode
from nodes.connection import NodeConnection, RawConnection


class RawWorkflow(TypedDict):
    name: str
    nodes: list[RawNode]
    connections: dict[str, list[RawConnection]]


class Workflow:
    def __init__(self, nodes: list[BaseNode], connections: list[NodeConnection]):
        self.nodes = nodes
        self.connections = connections

    def get_start_nodes(self) -> list[BaseNode]:
        # Assuming start nodes are those without any incoming connections
        nodes_as_target = {conn.to for conn in self.connections}
        start_nodes = [node for node in self.nodes if node not in nodes_as_target]

        return start_nodes

    async def execute_async(self, state: dict, variables: dict, **kwarg):
        nodes_to_exe = self.get_start_nodes()
        coroutine_list = []
        while nodes_to_exe:
            clone_variables = variables.copy()

            for node in nodes_to_exe:
                coroutine_list.append(
                    node.execute_async(state, clone_variables, **kwarg)
                )

            await asyncio.gather(*coroutine_list)

            next_nodes = []
            for node in nodes_to_exe:
                next_nodes.extend(await node.next_nodes(state, clone_variables))

            nodes_to_exe = next_nodes
            coroutine_list = []
