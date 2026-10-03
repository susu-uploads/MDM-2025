#!/usr/bin/env python3
"""Демонстрация работы паттерна Singleton."""

from __future__ import annotations

import sys
from typing import TextIO

from singleton import Singleton


def run(stdout: TextIO = sys.stdout) -> int:
    """Запускает демонстрационный сценарий из методических шагов.

    В сценарии создаются две переменные-ссылки, но фактически они
    указывают на один и тот же singleton-объект.
    """
    single_object = Singleton.get_instance()
    single_object.flag = True
    print(f"singleObject = {single_object.flag}", file=stdout)

    single_object1 = Singleton.get_instance()
    single_object1.flag = False
    print(f"singleObject = {single_object.flag}", file=stdout)

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
