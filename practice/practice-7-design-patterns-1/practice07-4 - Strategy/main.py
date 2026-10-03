#!/usr/bin/env python3
"""Консольная демонстрация паттерна Strategy для отчета по арендам."""

from __future__ import annotations

import sys
from typing import TextIO

from customer import Customer
from movie import Movie, MovieType
from rental import Rental
from statements import HTMLStatement, Statement, TextStatement


def parse_strategy(raw_value: str) -> Statement:
    """Выбирает стратегию отчета по идентификатору формата."""
    strategy_name = raw_value.strip().lower()
    if strategy_name == "text":
        return TextStatement()
    if strategy_name == "html":
        return HTMLStatement()
    raise ValueError("неизвестный формат отчета")


def parse_rental_line(raw_value: str) -> Rental:
    """Парсит строку аренды формата: `title;movie_type;days`."""
    parts = [part.strip() for part in raw_value.split(";")]
    if len(parts) != 3:
        raise ValueError("ожидается формат title;movie_type;days")

    title, movie_type_raw, days_raw = parts
    movie_type = MovieType(movie_type_raw)
    days = int(days_raw)

    return Rental(movie=Movie(title=title, movie_type=movie_type), days_rented=days)


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает однократное формирование отчета арендатора."""
    strategy_line = stdin.readline()
    customer_name_line = stdin.readline()

    if not strategy_line or not customer_name_line:
        print("Ошибка ввода!", file=stderr)
        return 1

    try:
        statement = parse_strategy(strategy_line)
        customer = Customer(name=customer_name_line.strip())

        for line in stdin:
            if not line.strip():
                break
            customer.add_rental(parse_rental_line(line))

        print(customer.get_statement_value(statement), file=stdout)
    except (TypeError, ValueError):
        print("Ошибка ввода!", file=stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
