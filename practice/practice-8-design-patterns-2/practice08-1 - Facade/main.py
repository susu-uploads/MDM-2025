#!/usr/bin/env python3
"""Консольная точка входа для расчета страхового взноса через Facade."""

from __future__ import annotations

import sys
from typing import TextIO

from calculation_facade import CalculationFacade, Estate, EstateType, ValueGroup


def parse_estate(line: str) -> Estate:
    """Преобразует строку ввода в объект `Estate`.

    Формат строки:
    `estate_type area_m2 cadastral_value residents_count value_group`

    Пример:
    `apartment 60 5000000 3 comfort`
    """
    parts = line.strip().split()
    if len(parts) != 5:
        raise ValueError("ожидается 5 параметров")

    estate_type_raw, area_raw, cadastral_raw, residents_raw, value_group_raw = parts

    try:
        estate_type = EstateType(estate_type_raw)
        value_group = ValueGroup(value_group_raw)
        area_m2 = float(area_raw)
        cadastral_value = float(cadastral_raw)
        residents_count = int(residents_raw)
    except (TypeError, ValueError) as error:
        raise ValueError("некорректные данные объекта недвижимости") from error

    return Estate(
        estate_type=estate_type,
        area_m2=area_m2,
        cadastral_value=cadastral_value,
        residents_count=residents_count,
        value_group=value_group,
    )


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает однократный расчет страхового взноса."""
    line = stdin.readline()
    if not line:
        print("Ошибка ввода!", file=stderr)
        return 1

    try:
        estate = parse_estate(line)
        amount = CalculationFacade().calculate_contribution(estate)
    except (TypeError, ValueError):
        print("Ошибка ввода!", file=stderr)
        return 1

    print(f"{amount:.2f}", file=stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
