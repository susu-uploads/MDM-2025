#!/usr/bin/env python3
"""Консольная демонстрация Abstract Factory для создания врагов."""

from __future__ import annotations

import sys
from typing import TextIO

from difficulty_level import DifficultyLevel
from enemies import Monster, Soldier, SuperMonster
from enemy_factory import create_factory, make_named_enemy


def parse_input(line: str) -> tuple[DifficultyLevel, type[Soldier | Monster | SuperMonster], str]:
    """Парсит строку формата: `difficulty enemy_type name`."""
    parts = line.strip().split()
    if len(parts) < 3:
        raise ValueError("ожидается: difficulty enemy_type name")

    difficulty_raw = parts[0].lower()
    enemy_type_raw = parts[1].lower()
    name = " ".join(parts[2:]).strip()

    difficulty = DifficultyLevel(difficulty_raw)

    enemy_type_map: dict[str, type[Soldier | Monster | SuperMonster]] = {
        "soldier": Soldier,
        "monster": Monster,
        "supermonster": SuperMonster,
    }
    enemy_type = enemy_type_map.get(enemy_type_raw)
    if enemy_type is None:
        raise ValueError("неизвестный enemy_type")

    return difficulty, enemy_type, name


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает однократное создание врага через фабрику."""
    line = stdin.readline()
    if not line:
        print("Ошибка ввода!", file=stderr)
        return 1

    try:
        difficulty, enemy_type, name = parse_input(line)
        factory = create_factory(difficulty)
        enemy = make_named_enemy(factory, enemy_type, name)
    except (TypeError, ValueError):
        print("Ошибка ввода!", file=stderr)
        return 1

    print(enemy, file=stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
