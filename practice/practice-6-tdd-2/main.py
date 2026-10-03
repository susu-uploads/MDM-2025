#!/usr/bin/env python3
"""Консольный запуск игры «Однобросковый боулинг».

Приложение принимает броски по одному.
В интерактивном режиме после каждого броска печатает текущий счет.
"""

from __future__ import annotations

import sys
from typing import TextIO

from bowling import Game


def parse_pins(raw_value: str) -> int:
    """Преобразует строку пользователя в количество сбитых кеглей.

    Args:
        raw_value: Строка, введенная пользователем.

    Returns:
        Целое значение кеглей.

    Raises:
        ValueError: Если строка пустая или не является корректным числом.
    """
    value = raw_value.strip()
    if not value:
        raise ValueError("пустой ввод")
    return int(value)


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает режим ввода бросков и подсчета очков.

    Args:
        stdin: Поток стандартного ввода.
        stdout: Поток стандартного вывода.
        stderr: Поток ошибок.

    Returns:
        Код завершения: 0 при успехе, 1 при ошибке ввода.
    """
    game = Game()
    interactive = stdin.isatty()

    if interactive:
        print("Введите количество сбитых кеглей для каждого броска (0..10).", file=stdout)
        print("Пустая строка завершает ввод досрочно.", file=stdout)

    while not game.is_finished:
        if interactive:
            print(f"Фрейм {game.get_current_frame()}, бросок: ", end="", file=stdout, flush=True)

        raw_value = stdin.readline()
        if raw_value == "":
            break
        if not raw_value.strip():
            break

        try:
            pins = parse_pins(raw_value)
            game.add(pins)
        except (TypeError, ValueError):
            print("Ошибка ввода!", file=stderr)
            return 1

        if interactive:
            print(f"Текущий счет: {game.get_score()}", file=stdout)

    print(game.get_score(), file=stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
