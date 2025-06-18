from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from typing import Union, Dict, Type
from app.exceptions import ValidationError

Number = Union[int, float, Decimal]


class Operation(ABC):
    @abstractmethod
    def execute(self, a: Number, b: Number) -> Number:
        pass  # pragma: no cover

    def __str__(self) -> str:
        return self.__class__.__name__


class Addition(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        return Decimal(a) + Decimal(b)


class Subtraction(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        return Decimal(a) - Decimal(b)


class Multiplication(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        return Decimal(a) * Decimal(b)


class Division(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        if Decimal(b) == 0:
            raise ValidationError("Division by zero is not allowed")
        return Decimal(a) / Decimal(b)


class Power(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        if Decimal(b) < 0:
            raise ValidationError("Negative exponents not supported")
        return Decimal(a) ** Decimal(b)


class Root(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        if Decimal(b) == 0:
            raise ValidationError("Zero root is undefined")
        if Decimal(a) < 0 and int(b) % 2 == 0:
            raise ValidationError("Cannot calculate root of negative number")
        try:
            result = Decimal(a) ** (Decimal(1) / Decimal(b))
            return result.quantize(Decimal('1.000000000000000000'))
        except (ZeroDivisionError, InvalidOperation):
            raise ValidationError("Invalid root operation")


class OperationFactory:
    _operations: Dict[str, Type[Operation]] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
    }

    @staticmethod
    def create_operation(name: str) -> Operation:
        operation_cls = OperationFactory._operations.get(name.lower())
        if not operation_cls:
            raise ValueError(f"Unknown operation: {name}")
        return operation_cls()

    @staticmethod
    def register_operation(name: str, operation_cls: Type[Operation]) -> None:
        if not issubclass(operation_cls, Operation):
            raise TypeError("Operation class must inherit from Operation base class")
        OperationFactory._operations[name.lower()] = operation_cls
