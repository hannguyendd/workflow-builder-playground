from nodes.base import BaseNode
from nodes.builders.connection import ConnectionBuilder
from nodes.connection import NodeConnection
from nodes.factory import NodeFactory
from workflows.base import RawWorkflow, Workflow


class WorkflowBuilder:
    state: dict = {}
    variables: dict = {}

    def __init__(self, params: RawWorkflow):
        self.name = params.get("name", "Unnamed Workflow")
        self.raw_nodes = params.get("nodes", [])
        self.raw_connections = params.get("connections", [])

    def build(self) -> "Workflow":
        nodes: list[BaseNode] = []
        node_factory = NodeFactory()
        for item in self.raw_nodes:
            node = node_factory.create_node(
                item.get("type", "unknown"),
                item.get("name", "Unnamed Node"),
                item.get("description", ""),
                item.get("parameters", {}),
            )
            nodes.append(node)

        node_map = {node.name: node for node in nodes}
        connections: list[NodeConnection] = []
        for node_name, raw_conns in self.raw_connections:
            node_connections: list[NodeConnection] = []
            node = node_map.get(node_name)
            if not node:
                raise ValueError(f"Node with name {node_name} not found.")

            for raw_conn in raw_conns:
                connection = ConnectionBuilder.build(raw_conn, node_map)
                connections.append(connection)
                node_connections.append(connection)

            node.set_connections(node_connections)

        workflow = Workflow(nodes, connections)
        workflow.name = self.name
        # Implement the logic to convert nodes and connections into a Workflow instance
        return workflow
