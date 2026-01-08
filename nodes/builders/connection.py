from nodes.base import BaseNode
from nodes.connection import NodeConnection, RawConnection


class ConnectionBuilder:
    @staticmethod
    def build(
        raw_connection: RawConnection, nodes_dict: dict[str, BaseNode]
    ) -> NodeConnection:
        to_node = nodes_dict.get(raw_connection["to"])
        if not to_node:
            raise ValueError(f"Node with name {raw_connection['to']} not found.")
        return NodeConnection(to=to_node, label=raw_connection["label"])
