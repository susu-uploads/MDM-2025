"""Unit-тесты для паттерна Builder (генератор электронной книги)."""

from __future__ import annotations

import tempfile
import unittest
from io import StringIO
from pathlib import Path

from builders import FB2BookBuilder, HTMLBookBuilder
from composer import BookComposer
from generate_romeo_and_juliet import RomeoAndJulietComposer
from main import run


class TestHTMLBookBuilder(unittest.TestCase):
    """Проверяет корректность построения HTML-книги."""

    def test_nested_sections_and_delimiter(self) -> None:
        """Проверяет заголовки, абзацы и разделитель в HTML."""
        builder = HTMLBookBuilder()
        builder.begin_section("Глава 1")
        builder.begin_section("Сцена 1")
        builder.add_paragraph("Текст")
        builder.add_delimiter()
        builder.end_section()
        builder.begin_section("Сцена 2")
        builder.add_paragraph("Ещё текст")

        expected = (
            "<h1>Глава 1</h1>"
            "<h2>Сцена 1</h2>"
            "<p>Текст</p>"
            "<hr>"
            "<h2>Сцена 2</h2>"
            "<p>Ещё текст</p>"
        )
        self.assertEqual(expected, builder.get_result())

    def test_end_section_not_below_level_one(self) -> None:
        """Проверяет, что уровень раздела не опускается ниже h1."""
        builder = HTMLBookBuilder()
        builder.end_section()
        builder.begin_section("Начало")
        self.assertEqual("<h1>Начало</h1>", builder.get_result())

    def test_html_escapes_special_characters(self) -> None:
        """Проверяет экранирование спецсимволов в HTML."""
        builder = HTMLBookBuilder()
        builder.begin_section("5 < 7 & 8")
        builder.add_paragraph("A & B < C")
        self.assertEqual(
            "<h1>5 &lt; 7 &amp; 8</h1><p>A &amp; B &lt; C</p>",
            builder.get_result(),
        )


class TestFB2BookBuilder(unittest.TestCase):
    """Проверяет корректность построения FB2-книги."""

    def test_simple_section_output(self) -> None:
        """Проверяет базовый сценарий генерации FB2-секции."""
        builder = FB2BookBuilder()
        builder.begin_section("Раздел")
        builder.add_paragraph("Абзац")
        builder.add_delimiter()
        builder.end_section()

        expected = (
            "<section><title>Раздел</title>"
            "<p>Абзац</p>"
            "<p>* * *</p>"
            "</section>"
        )
        self.assertEqual(expected, builder.get_result())

    def test_fb2_escapes_special_characters(self) -> None:
        """Проверяет экранирование спецсимволов в FB2/XML."""
        builder = FB2BookBuilder()
        builder.begin_section("5 < 7 & 8")
        builder.add_paragraph("A & B < C")
        builder.end_section()
        self.assertEqual(
            "<section><title>5 &lt; 7 &amp; 8</title><p>A &amp; B &lt; C</p></section>",
            builder.get_result(),
        )


class TestBookComposer(unittest.TestCase):
    """Проверяет абстракцию BookComposer и concrete-компоновщик."""

    def test_book_composer_is_abstract(self) -> None:
        """Проверяет, что абстрактный компоновщик нельзя создать напрямую."""
        with self.assertRaises(TypeError):
            BookComposer()

    def test_compose_book_for_html_builder(self) -> None:
        """Проверяет, что директор формирует ожидаемую HTML-структуру."""
        composer = RomeoAndJulietComposer()
        builder = HTMLBookBuilder()
        composer.compose_book(builder)

        expected = (
            "<h1>Ромео и Джульетта</h1>"
            "<h2>Пролог</h2>"
            "<p>Две равно уважаемых семьи</p>"
            "<p>В Вероне, где встречают нас события,</p>"
            "<hr>"
            "<h2>Акт I</h2>"
            "<p>Мятежные вновь вспыхивают раздоры...</p>"
        )
        self.assertEqual(expected, builder.get_result())

    def test_compose_book_for_fb2_builder(self) -> None:
        """Проверяет, что директор формирует ожидаемую FB2-структуру."""
        composer = RomeoAndJulietComposer()
        builder = FB2BookBuilder()
        composer.compose_book(builder)

        expected = (
            "<section><title>Ромео и Джульетта</title>"
            "<section><title>Пролог</title>"
            "<p>Две равно уважаемых семьи</p>"
            "<p>В Вероне, где встречают нас события,</p>"
            "<p>* * *</p>"
            "</section>"
            "<section><title>Акт I</title>"
            "<p>Мятежные вновь вспыхивают раздоры...</p>"
            "</section>"
            "</section>"
        )
        self.assertEqual(expected, builder.get_result())

    def test_create_html_book_writes_file(self) -> None:
        """Проверяет запись HTML-результата в файл."""
        composer = RomeoAndJulietComposer()
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "book.html"
            result = composer.create_html_book(target)
            self.assertTrue(target.exists())
            self.assertEqual(result, target.read_text(encoding="utf-8"))
            self.assertIn("<h1>Ромео и Джульетта</h1>", result)

    def test_create_fb2_book_writes_file(self) -> None:
        """Проверяет запись FB2-результата в файл."""
        composer = RomeoAndJulietComposer()
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "book.fb2"
            result = composer.create_fb2_book(target)
            self.assertTrue(target.exists())
            self.assertEqual(result, target.read_text(encoding="utf-8"))
            self.assertIn("<section><title>Ромео и Джульетта</title>", result)


class TestCLI(unittest.TestCase):
    """Проверяет запуск приложения через `run` генератора."""

    def test_run_html_generation(self) -> None:
        """Проверяет успешный запуск генерации HTML-файла."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "output.html"
            stdout = StringIO()
            stderr = StringIO()

            code = run(["html", str(output_path)], stdout=stdout, stderr=stderr)

            self.assertEqual(0, code)
            self.assertTrue(output_path.exists())
            self.assertIn("Файл успешно создан", stdout.getvalue())
            self.assertEqual("", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
