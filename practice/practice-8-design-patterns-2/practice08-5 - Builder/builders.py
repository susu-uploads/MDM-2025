"""Реализации паттерна Builder для генерации электронной книги."""

from __future__ import annotations

from abc import ABC, abstractmethod
from html import escape


class BookBuilder(ABC):
    """Абстрактный интерфейс билдера книги."""

    @abstractmethod
    def begin_section(self, title: str) -> None:
        """Открывает новый раздел с заголовком."""
        ...

    @abstractmethod
    def end_section(self) -> None:
        """Закрывает текущий раздел."""
        ...

    @abstractmethod
    def add_paragraph(self, text: str) -> None:
        """Добавляет абзац в текущий раздел."""
        ...

    @abstractmethod
    def add_delimiter(self) -> None:
        """Добавляет смысловой разделитель внутри раздела."""
        ...

    @abstractmethod
    def get_result(self) -> str:
        """Возвращает итоговый результат в виде строки."""
        ...


class HTMLBookBuilder(BookBuilder):
    """Билдер электронной книги в формате HTML."""

    def __init__(self) -> None:
        """Инициализирует внутреннее состояние билдера."""
        self._parts: list[str] = []
        self._section_level = 1

    def begin_section(self, title: str) -> None:
        """Добавляет заголовок раздела с учетом уровня вложенности."""
        safe_title = escape(title)
        level = min(self._section_level, 6)
        self._parts.append(f"<h{level}>{safe_title}</h{level}>")
        self._section_level += 1

    def end_section(self) -> None:
        """Снижает уровень вложенности раздела."""
        if self._section_level > 1:
            self._section_level -= 1

    def add_paragraph(self, text: str) -> None:
        """Добавляет HTML-абзац."""
        safe_text = escape(text)
        self._parts.append(f"<p>{safe_text}</p>")

    def add_delimiter(self) -> None:
        """Добавляет горизонтальный разделитель."""
        self._parts.append("<hr>")

    def get_result(self) -> str:
        """Возвращает итоговый HTML-текст книги."""
        return "".join(self._parts)


class FB2BookBuilder(BookBuilder):
    """Билдер электронной книги в формате FB2/XML."""

    def __init__(self) -> None:
        """Инициализирует внутреннее состояние билдера."""
        self._parts: list[str] = []

    def begin_section(self, title: str) -> None:
        """Открывает секцию FB2 с заголовком."""
        safe_title = escape(title)
        self._parts.append(f"<section><title>{safe_title}</title>")

    def end_section(self) -> None:
        """Закрывает секцию FB2."""
        self._parts.append("</section>")

    def add_paragraph(self, text: str) -> None:
        """Добавляет FB2-абзац."""
        safe_text = escape(text)
        self._parts.append(f"<p>{safe_text}</p>")

    def add_delimiter(self) -> None:
        """Добавляет разделитель в формате FB2."""
        self._parts.append("<p>* * *</p>")

    def get_result(self) -> str:
        """Возвращает итоговый FB2-текст книги."""
        return "".join(self._parts)
