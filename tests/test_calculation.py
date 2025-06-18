import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_addition():
    calc = Calculation(operation="Addition", operand1=Decimal("7"), operand2=Decimal("4"))
    assert calc.result == Decimal("11")


def test_subtraction():
    calc = Calculation(operation="Subtraction", operand1=Decimal("10"), operand2=Decimal("6"))
    assert calc.result == Decimal("4")


def test_multiplication():
    calc = Calculation(operation="Multiplication", operand1=Decimal("3"), operand2=Decimal("5"))
    assert calc.result == Decimal("15")


def test_division():
    calc = Calculation(operation="Division", operand1=Decimal("9"), operand2=Decimal("3"))
    assert calc.result == Decimal("3")


def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Division", operand1=Decimal("6"), operand2=Decimal("0"))


def test_power():
    calc = Calculation(operation="Power", operand1=Decimal("3"), operand2=Decimal("2"))
    assert calc.result == Decimal("9")


def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", operand1=Decimal("5"), operand2=Decimal("-2"))


def test_root():
    calc = Calculation(operation="Root", operand1=Decimal("81"), operand2=Decimal("4"))
    assert calc.result == Decimal("3")


def test_invalid_root():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation(operation="Root", operand1=Decimal("-25"), operand2=Decimal("2"))


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Square", operand1=Decimal("5"), operand2=Decimal("5"))


def test_to_dict():
    calc = Calculation(operation="Addition", operand1=Decimal("10"), operand2=Decimal("15"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "operand1": "10",
        "operand2": "15",
        "result": "25",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "12",
        "operand2": "18",
        "result": "30",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("12")
    assert calc.operand2 == Decimal("18")
    assert calc.result == Decimal("30")


def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "oops",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(operation="Division", operand1=Decimal("5"), operand2=Decimal("6"))
    assert calc.format_result(precision=2) == "0.83"
    assert calc.format_result(precision=5) == "0.83333"


def test_equality():
    calc1 = Calculation(operation="Multiplication", operand1=Decimal("3"), operand2=Decimal("4"))
    calc2 = Calculation(operation="Multiplication", operand1=Decimal("3"), operand2=Decimal("4"))
    calc3 = Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("2"))
    assert calc1 == calc2
    assert calc1 != calc3


def test_from_dict_result_mismatch(caplog):
    """Logs a warning if result in saved data doesn't match recomputed result."""
    data = {
        "operation": "Addition",
        "operand1": "4",
        "operand2": "6",
        "result": "20",  # Incorrect on purpose
        "timestamp": datetime.now().isoformat()
    }

    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    assert "Loaded result 20 != computed 10" in caplog.text

