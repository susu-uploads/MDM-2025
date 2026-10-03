"""Базовый абстрактный компоновщик книги через интерфейс билдера."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from builders import BookBuilder, FB2BookBuilder, HTMLBookBuilder


class BookComposer(ABC):
    """Абстрактный директор для сборки книги через билдер."""

    @abstractmethod
    def compose_book(self, book_builder: BookBuilder) -> None:
        """Заполняет книгу содержимым.

        Args:
            book_builder: Конкретная реализация билдера (HTML/FB2).
        """
        ...

    def create_fb2_book(self, file_name: str | Path) -> str:
        """Собирает FB2-книгу и сохраняет результат в файл.

        Args:
            file_name: Путь, по которому нужно сохранить результат.

        Returns:
            Содержимое записанного файла.
        """
        builder = FB2BookBuilder()
        self.compose_book(builder)
        result = builder.get_result()
        Path(file_name).write_text(result, encoding="utf-8")
        return result

    def create_html_book(self, file_name: str | Path) -> str:
        """Собирает HTML-книгу и сохраняет результат в файл.

        Args:
            file_name: Путь, по которому нужно сохранить результат.

        Returns:
            Содержимое записанного файла.
        """
        builder = HTMLBookBuilder()
        self.compose_book(builder)
        result = builder.get_result()
        Path(file_name).write_text(result, encoding="utf-8")
        return result
