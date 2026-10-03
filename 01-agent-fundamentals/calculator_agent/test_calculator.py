import pytest

from calculator import calculator


def test_addition():
    result = calculator("add", 1, 5)

    assert result == 6


def test_subtraction():
    result = calculator("subtract", 5, 1)

    assert result == 4


def test_multiplication():
    result = calculator("multiply", 2, 5)

    assert result == 10


def test_division():
    result = calculator("divide", 10, 2)

    assert result == 5


def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator("divide", 10, 0)


def test_unsupported_operation():
    with pytest.raises(ValueError, match="Unsupported operation"):
        calculator("power", 2, 3)