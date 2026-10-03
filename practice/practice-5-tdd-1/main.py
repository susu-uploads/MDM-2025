#!/usr/bin/env python3
"""Точка входа консольного приложения для вычисления Fibonacci."""

from __future__ import annotations

import sys
from typing import TextIO

from fibonacci import Fibonacci


def parse_input(raw_value: str) -> int:
    """Преобразует пользовательский ввод в целочисленный индекс.

    Args:
        raw_value: Сырая строка, прочитанная из stdin.

    Returns:
        Распарсенный целочисленный индекс.

    Raises:
        ValueError: Если строка пустая или не приводится к ``int``.
    """
    value = raw_value.strip()
    if not value:
        raise ValueError("пустой ввод")
    return int(value)


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает однократный консольный расчет числа Fibonacci.

    Args:
        stdin: Поток входных данных.
        stdout: Поток стандартного вывода.
        stderr: Поток ошибок.

    Returns:
        Код завершения процесса: ``0`` при успехе, ``1`` при ошибке ввода.
    """
    raw_value = stdin.readline()

    try:
        index = parse_input(raw_value)
        result = Fibonacci.fibonacci(index)
    except (TypeError, ValueError):
        print("Ошибка ввода!", file=stderr)
        return 1

    print(result, file=stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
