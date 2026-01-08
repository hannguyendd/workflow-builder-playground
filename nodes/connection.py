from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from nodes.base import BaseNode


class RawConnection(TypedDict):
    to: str  # node name
    label: str


class NodeConnection:
    to: "BaseNode"
    label: str = "main"

    def __init__(self, to: "BaseNode", label="main"):
        self.to = to
        self.label = label
