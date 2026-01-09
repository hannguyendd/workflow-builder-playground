import asyncio
from typing import TypedDict
from nodes.base import BaseNode, RawNode
from nodes.connection import NodeConnection, RawConnection
from workflows.context import ExecutionContext


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

    async def execute_async(
        self,
        ctx: ExecutionContext | None = None,
        state: dict | None = None,
        config: dict | None = None,
    ) -> ExecutionContext:
        """
        Execute the workflow asynchronously.

        Args:
            ctx: Optional ExecutionContext. If not provided, one will be created.
            state: Optional initial state (used if ctx is not provided).
            config: Optional config (used if ctx is not provided).

        Returns:
            The ExecutionContext after workflow completion.
        """
        if ctx is None:
            ctx = ExecutionContext(
                state=state or {},
                config=config or {},
            )

        nodes_to_exe = self.get_start_nodes()
        coroutine_list = []

        while nodes_to_exe:
            for node in nodes_to_exe:
                coroutine_list.append(node.execute_async(ctx))

            await asyncio.gather(*coroutine_list)

            next_nodes = []
            for node in nodes_to_exe:
                next_nodes.extend(await node.next_nodes(ctx))

            nodes_to_exe = next_nodes
            coroutine_list = []

        return ctx
