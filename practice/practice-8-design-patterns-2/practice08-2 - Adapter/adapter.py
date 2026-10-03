"""Реализация паттерна Adapter для ElSimpleSSHClient."""

from __future__ import annotations

from ssh_client import ElSimpleSSHClient
from ssh_tunnel import SSHTunnel


class SecureBlackboxSSHTunnelAdapter(SSHTunnel):
    """Адаптирует `ElSimpleSSHClient` к интерфейсу `SSHTunnel`."""

    def __init__(self) -> None:
        self._ssh_client = ElSimpleSSHClient()
        self._ssh_client.use_internal_socket = True

    @property
    def local_port(self) -> int:
        return self._ssh_client.bind_port

    @local_port.setter
    def local_port(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("local_port должен быть целым числом")
        if not 1 <= value <= 65535:
            raise ValueError("local_port должен быть в диапазоне 1..65535")
        self._ssh_client.bind_port = value

    @property
    def remote_host(self) -> str:
        return self._ssh_client.destination_host

    @remote_host.setter
    def remote_host(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("remote_host должен быть строкой")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("remote_host не должен быть пустым")
        self._ssh_client.destination_host = cleaned

    @property
    def remote_port(self) -> int:
        return self._ssh_client.destination_port

    @remote_port.setter
    def remote_port(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("remote_port должен быть целым числом")
        if not 1 <= value <= 65535:
            raise ValueError("remote_port должен быть в диапазоне 1..65535")
        self._ssh_client.destination_port = value

    def open(self) -> None:
        self._ssh_client.connect()

    def close(self) -> None:
        self._ssh_client.disconnect()
