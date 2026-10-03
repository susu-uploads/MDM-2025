#!/usr/bin/env python3
"""Консольная демонстрация работы адаптера SSH-туннеля."""

from __future__ import annotations

import sys
from typing import TextIO

from adapter import SecureBlackboxSSHTunnelAdapter


def parse_input(line: str) -> tuple[int, str, int]:
    """Парсит строку формата: `local_port remote_host remote_port`."""
    parts = line.strip().split()
    if len(parts) != 3:
        raise ValueError("ожидается 3 параметра")

    local_port_raw, remote_host, remote_port_raw = parts
    local_port = int(local_port_raw)
    remote_port = int(remote_port_raw)
    return local_port, remote_host, remote_port


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr) -> int:
    """Запускает однократную настройку и открытие/закрытие туннеля."""
    line = stdin.readline()
    if not line:
        print("Ошибка ввода!", file=stderr)
        return 1

    adapter = SecureBlackboxSSHTunnelAdapter()

    try:
        local_port, remote_host, remote_port = parse_input(line)
        adapter.local_port = local_port
        adapter.remote_host = remote_host
        adapter.remote_port = remote_port
        adapter.open()
        adapter.close()
    except (TypeError, ValueError):
        print("Ошибка ввода!", file=stderr)
        return 1

    print(
        f"Tunnel configured: local={adapter.local_port}, "
        f"remote={adapter.remote_host}:{adapter.remote_port}",
        file=stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
