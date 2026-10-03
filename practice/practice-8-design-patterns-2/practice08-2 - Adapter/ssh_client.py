"""Эмуляция стороннего класса ElSimpleSSHClient из SecureBlackBox.

В реальном проекте это внешний библиотечный класс с несовместимым API.
"""

from __future__ import annotations


class ElSimpleSSHClient:
    """Упрощенная модель внешнего SSH-клиента."""

    def __init__(self) -> None:
        self.use_internal_socket: bool = False
        self.bind_port: int = 0
        self.destination_host: str = ""
        self.destination_port: int = 0
        self.is_connected: bool = False

    def connect(self) -> None:
        """Открывает соединение внешнего клиента."""
        self.is_connected = True

    def disconnect(self) -> None:
        """Закрывает соединение внешнего клиента."""
        self.is_connected = False
