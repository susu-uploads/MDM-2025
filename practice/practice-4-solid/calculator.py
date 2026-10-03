"""Доменная логика калькулятора с архитектурой по принципам SOLID.

Модуль не занимается консольным вводом/выводом и форматированием строк.
Он содержит только:
- разбор математического выражения;
- выбор операции;
- вычисление результата;
- генерацию доменных исключений.
"""

from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


class CalculatorError(Exception):
    """Базовое исключение доменной модели калькулятора.

    Attributes:
        message: Человекочитаемый текст ошибки.
    """

    message: str = "Ошибка"

    def __str__(self) -> str:
        return self.message


class InputFormatError(CalculatorError):
    """Ошибка формата входной строки."""

    message: str = "Ошибка ввода!"


class DivisionByZeroError(CalculatorError):
    """Ошибка деления на ноль."""

    message: str = "Невозможно выполнить деление на ноль!"


class NegativeSqrtError(CalculatorError):
    """Ошибка извлечения корня из отрицательного числа."""

    message: str = "Невозможно выполнить извлечение квадратного корня из отрицательного числа!"


class BinaryOperation(ABC):
    """Интерфейс для бинарных операций."""

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Возвращает символьное имя операции (например, `+`)."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, left: float, right: float) -> float:
        """Выполняет бинарную операцию.

        Args:
            left: Левый операнд.
            right: Правый операнд.

        Returns:
            Результат вычисления.
        """
        raise NotImplementedError


class UnaryOperation(ABC):
    """Интерфейс для унарных операций."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает имя функции (например, `sqrt`)."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, value: float) -> float:
        """Выполняет унарную операцию.

        Args:
            value: Значение операнда.

        Returns:
            Результат вычисления.
        """
        raise NotImplementedError


class AddOperation(BinaryOperation):
    """Операция сложения."""

    @property
    def symbol(self) -> str:
        return "+"

    def execute(self, left: float, right: float) -> float:
        return left + right


class SubtractOperation(BinaryOperation):
    """Операция вычитания."""

    @property
    def symbol(self) -> str:
        return "-"

    def execute(self, left: float, right: float) -> float:
        return left - right


class MultiplyOperation(BinaryOperation):
    """Операция умножения."""

    @property
    def symbol(self) -> str:
        return "*"

    def execute(self, left: float, right: float) -> float:
        return left * right


class DivideOperation(BinaryOperation):
    """Операция деления."""

    @property
    def symbol(self) -> str:
        return "/"

    def execute(self, left: float, right: float) -> float:
        if right == 0:
            raise DivisionByZeroError
        return left / right


class SqrtOperation(UnaryOperation):
    """Операция извлечения квадратного корня."""

    @property
    def name(self) -> str:
        return "sqrt"

    def execute(self, value: float) -> float:
        if value < 0:
            raise NegativeSqrtError
        return math.sqrt(value)


class SquareOperation(UnaryOperation):
    """Операция возведения в квадрат."""

    @property
    def name(self) -> str:
        return "sqr"

    def execute(self, value: float) -> float:
        return value * value


@dataclass(frozen=True)
class BinaryExpression:
    """Результат разбора бинарного выражения."""

    operator: str
    left: float
    right: float


@dataclass(frozen=True)
class UnaryExpression:
    """Результат разбора унарного выражения."""

    function: str
    value: float


class ExpressionParser:
    """Отвечает только за разбор входной строки в структуру выражения."""

    _number: str = r"[-+]?(?:\d+(?:\.\d+)?|\.\d+)"
    _binary_re: re.Pattern[str] = re.compile(rf"^\s*({_number})\s*([+\-*/])\s*({_number})\s*$")
    _unary_re: re.Pattern[str] = re.compile(rf"^\s*([A-Za-z]+)\s*\(\s*({_number})\s*\)\s*$")

    def parse(self, expression: str) -> BinaryExpression | UnaryExpression:
        """Разбирает строку выражения в структурированный объект.

        Поддерживаемые форматы:
        - бинарный: `<число><оператор><число>` (например, `9/3`);
        - унарный: `<функция>(<число>)` (например, `sqrt(25)`).

        Args:
            expression: Входная строка пользователя.

        Returns:
            Экземпляр `BinaryExpression` или `UnaryExpression`.

        Raises:
            InputFormatError: Если строка не соответствует поддерживаемому формату.
        """
        binary_match = self._binary_re.match(expression)
        if binary_match:
            left, operator, right = binary_match.groups()
            return BinaryExpression(operator=operator, left=float(left), right=float(right))

        unary_match = self._unary_re.match(expression)
        if unary_match:
            function, value = unary_match.groups()
            return UnaryExpression(function=function.lower(), value=float(value))

        raise InputFormatError


class OperationRegistry:
    """Регистр операций: расширяется новыми операциями без изменения калькулятора."""

    def __init__(self, binary_operations: list[BinaryOperation], unary_operations: list[UnaryOperation]) -> None:
        """Создает реестр доступных операций.

        Args:
            binary_operations: Список реализаций бинарных операций.
            unary_operations: Список реализаций унарных операций.
        """
        self._binary_operations = {operation.symbol: operation for operation in binary_operations}
        self._unary_operations = {operation.name: operation for operation in unary_operations}

    def get_binary(self, symbol: str) -> BinaryOperation:
        """Возвращает бинарную операцию по ее символу.

        Args:
            symbol: Символ операции (`+`, `-`, `*`, `/`).

        Returns:
            Реализация бинарной операции.

        Raises:
            InputFormatError: Если операция не зарегистрирована.
        """
        operation = self._binary_operations.get(symbol)
        if operation is None:
            raise InputFormatError
        return operation

    def get_unary(self, name: str) -> UnaryOperation:
        """Возвращает унарную операцию по имени функции.

        Args:
            name: Имя функции (`sqrt`, `sqr`).

        Returns:
            Реализация унарной операции.

        Raises:
            InputFormatError: Если операция не зарегистрирована.
        """
        operation = self._unary_operations.get(name)
        if operation is None:
            raise InputFormatError
        return operation


class Calculator:
    """Вычисляет выражение, не зная деталей ввода/вывода."""

    def __init__(self, parser: ExpressionParser, registry: OperationRegistry) -> None:
        """Создает экземпляр калькулятора.

        Args:
            parser: Компонент разбора входного выражения.
            registry: Реестр операций.
        """
        self._parser = parser
        self._registry = registry

    def evaluate(self, expression: str) -> float:
        """Вычисляет результат математического выражения.

        Args:
            expression: Выражение пользователя в поддерживаемом формате.

        Returns:
            Числовой результат выражения.

        Raises:
            InputFormatError: Если выражение имеет неверный формат.
            DivisionByZeroError: Если выполняется деление на ноль.
            NegativeSqrtError: Если вычисляется `sqrt` от отрицательного числа.
        """
        parsed_expression = self._parser.parse(expression)
        if isinstance(parsed_expression, BinaryExpression):
            operation = self._registry.get_binary(parsed_expression.operator)
            return operation.execute(parsed_expression.left, parsed_expression.right)

        operation = self._registry.get_unary(parsed_expression.function)
        return operation.execute(parsed_expression.value)


def build_calculator() -> Calculator:
    """Собирает калькулятор со стандартным набором операций.

    Returns:
        Готовый к использованию экземпляр `Calculator`.
    """
    parser = ExpressionParser()
    registry = OperationRegistry(
        binary_operations=[
            AddOperation(),
            SubtractOperation(),
            MultiplyOperation(),
            DivideOperation(),
        ],
        unary_operations=[
            SqrtOperation(),
            SquareOperation(),
        ],
    )
    return Calculator(parser=parser, registry=registry)
