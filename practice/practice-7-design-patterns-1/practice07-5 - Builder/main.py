#!/usr/bin/env python3
"""CLI-точка входа для генерации книги «Ромео и Джульетта»."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence, TextIO

from generate_romeo_and_juliet import generate_romeo_and_juliet


def build_parser() -> argparse.ArgumentParser:
    """Создаёт и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Генерация книги «Ромео и Джульетта» в формате HTML/FB2",
    )
    parser.add_argument(
        "book_format",
        choices=("html", "fb2"),
        help="Формат выходной книги",
    )
    parser.add_argument(
        "output",
        help="Путь к выходному файлу",
    )
    return parser


def run(
    argv: Sequence[str] | None = None,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    """Точка входа CLI.

    Args:
        argv: Аргументы CLI без имени скрипта.
        stdout: Поток стандартного вывода.
        stderr: Поток вывода ошибок.

    Returns:
        Код завершения процесса.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    try:
        generate_romeo_and_juliet(args.book_format, output_path)
    except (OSError, ValueError) as error:
        print(f"Ошибка генерации: {error}", file=stderr)
        return 1

    print(f"Файл успешно создан: {output_path}", file=stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
