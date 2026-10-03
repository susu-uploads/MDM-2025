"""Интерфейс стандартного SSH-туннеля."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SSHTunnel(ABC):
    """Абстракция SSH-подключения, с которой работает клиентский код."""

    @property
    @abstractmethod
    def local_port(self) -> int:
        """Локальный порт для туннеля."""
        ...

    @local_port.setter
    @abstractmethod
    def local_port(self, value: int) -> None:
        """Устанавливает локальный порт туннеля."""
        ...

    @property
    @abstractmethod
    def remote_host(self) -> str:
        """Удаленный хост назначения."""
        ...

    @remote_host.setter
    @abstractmethod
    def remote_host(self, value: str) -> None:
        """Устанавливает удаленный хост назначения."""
        ...

    @property
    @abstractmethod
    def remote_port(self) -> int:
        """Удаленный порт назначения."""
        ...

    @remote_port.setter
    @abstractmethod
    def remote_port(self, value: int) -> None:
        """Устанавливает удаленный порт назначения."""
        ...

    @abstractmethod
    def open(self) -> None:
        """Открывает SSH-туннель."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Закрывает SSH-туннель."""
        ...
