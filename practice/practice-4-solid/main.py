#!/usr/bin/env python3
"""Точка входа консольного калькулятора."""

from __future__ import annotations

import sys
from typing import TextIO

from calculator import Calculator, CalculatorError, build_calculator


def format_result(value: float) -> str:
    """Преобразует числовой результат в строку для вывода.

    Args:
        value: Числовой результат вычисления.

    Returns:
        Строковое представление числа без лишней десятичной части.
    """
    if value.is_integer():
        return str(int(value))
    return f"{value:.10g}"


def evaluate_for_output(calculator: Calculator, expression: str) -> str:
    """Вычисляет выражение и возвращает строку для stdout.

    Args:
        calculator: Экземпляр калькулятора с доменной логикой.
        expression: Входная строка выражения.

    Returns:
        Результат вычисления или сообщение об ошибке в формате задания.
    """
    try:
        result = calculator.evaluate(expression)
        return format_result(result)
    except CalculatorError as error:
        return f"Сообщение: «{error}»"


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout) -> None:
    """Запускает цикл чтения выражений и печати результатов.

    Args:
        stdin: Поток входных данных.
        stdout: Поток выходных данных.
    """
    calculator = build_calculator()
    is_tty = stdin.isatty()

    if is_tty:
        expression = stdin.readline().strip()
        if expression:
            print(evaluate_for_output(calculator, expression), file=stdout)
        return

    for raw_line in stdin:
        expression = raw_line.strip()
        if not expression:
            continue
        print(evaluate_for_output(calculator, expression), file=stdout)


if __name__ == "__main__":
    run()
