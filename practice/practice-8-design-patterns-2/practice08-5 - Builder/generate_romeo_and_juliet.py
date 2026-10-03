"""Прикладная генерация книги «Ромео и Джульетта»."""

from __future__ import annotations

from pathlib import Path

from builders import BookBuilder
from composer import BookComposer


class RomeoAndJulietComposer(BookComposer):
    """Конкретный компоновщик для книги «Ромео и Джульетта»."""

    def compose_book(self, book_builder: BookBuilder) -> None:
        """Заполняет билдер структурой и фрагментами книги."""
        book_builder.begin_section("Ромео и Джульетта")
        book_builder.begin_section("Пролог")
        book_builder.add_paragraph("Две равно уважаемых семьи")
        book_builder.add_paragraph("В Вероне, где встречают нас события,")
        book_builder.add_delimiter()
        book_builder.end_section()

        book_builder.begin_section("Акт I")
        book_builder.add_paragraph("Мятежные вновь вспыхивают раздоры...")
        book_builder.end_section()
        book_builder.end_section()


def generate_romeo_and_juliet(book_format: str, output_path: str | Path) -> str:
    """Генерирует книгу «Ромео и Джульетта» в заданном формате.

    Args:
        book_format: Формат книги (`html` или `fb2`).
        output_path: Путь к выходному файлу.

    Returns:
        Содержимое сгенерированной книги.

    Raises:
        ValueError: Если передан неподдерживаемый формат.
    """
    composer = RomeoAndJulietComposer()
    target_path = Path(output_path)
    if book_format == "html":
        return composer.create_html_book(target_path)
    if book_format == "fb2":
        return composer.create_fb2_book(target_path)
    raise ValueError("неизвестный формат книги")
