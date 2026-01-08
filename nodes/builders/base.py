from abc import abstractmethod
from typing import Generator, Generic, TypeVar

from nodes.base import BaseNode
from nodes.exceptions import NodeValidationException

T = TypeVar("NODE_TYPE", bound=BaseNode)


class NodeBuilder(Generic[T]):
    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict = {},
        connections: list[dict] = [],
    ):
        self.name = name
        self.description = description
        self.parameters = parameters

    @abstractmethod
    def create(self) -> T:
        pass

    def build(self) -> T:
        error = self.get_error()
        if error:
            raise NodeValidationException(T.__name__, error, self.parameters)

        return self.create()

    def get_errors(self) -> Generator[str, None, None]:
        pass

    def get_error(self) -> str | None:
        return next(self.get_errors(), None)

    def is_valid(self) -> bool:
        return not any(self.get_errors())
