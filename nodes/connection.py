from enum import StrEnum
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from nodes.base import BaseNode


class ConnectionLabel(StrEnum):
    """Constants for connection labels to avoid typos."""

    MAIN = "main"
    TRUE = "true"
    FALSE = "false"
    BODY = "body"
    EXIT = "exit"


class RawConnection(TypedDict):
    to: str  # node name
    label: str


class NodeConnection:
    to: "BaseNode"
    label: str = "main"

    def __init__(self, to: "BaseNode", label="main"):
        self.to = to
        self.label = label
