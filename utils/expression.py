from abc import ABC, abstractmethod
from enum import Enum


class ConditionOperator(Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="


class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"


class AppExpression(ABC):
    @abstractmethod
    def to_expression(self) -> str:
        pass


class ConditionExpression(AppExpression):
    def __init__(self, left: str, operator: ConditionOperator, right: str):
        # validate operator
        if not isinstance(operator, ConditionOperator):
            raise ValueError("Invalid condition operator")

        self.left = left
        self.operator = operator
        self.right = right

    def to_expression(self) -> str:
        return f"{self.left} {self.operator.value} {self.right}"


class LogicalExpression(AppExpression):
    def __init__(self, operator: LogicalOperator, expressions: list[AppExpression]):
        # validate operator
        if not isinstance(operator, LogicalOperator):
            raise ValueError("Invalid logical operator")

        self.operator = operator
        self.expressions = expressions

    def to_expression(self) -> str:
        return f"( {
            f' {self.operator.value} '.join(
                [expr.to_expression() for expr in self.expressions]
            )
        } )"
