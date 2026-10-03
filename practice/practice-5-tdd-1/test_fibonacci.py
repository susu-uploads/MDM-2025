"""Набор тестов для практики TDD-1 по числам Fibonacci."""

from __future__ import annotations

import unittest

from fibonacci import Fibonacci


class TestFibonacci(unittest.TestCase):
    """Повторяет последовательность TDD-шагов из C# методички на Python."""

    def test_first_fibonacci_number(self) -> None:
        """Первый тест из методички: Fibonacci(0) == 0."""
        self.assertEqual(0, Fibonacci.fibonacci(0))

    def test_second_fibonacci_number(self) -> None:
        """Второй тест из методички: Fibonacci(1) == 1."""
        self.assertEqual(1, Fibonacci.fibonacci(1))

    def test_third_fibonacci_number(self) -> None:
        """Третий тест из методички: Fibonacci(2) == 1."""
        self.assertEqual(1, Fibonacci.fibonacci(2))

    def test_fourth_fibonacci_number(self) -> None:
        """Четвертый тест из методички: Fibonacci(3) == 2."""
        self.assertEqual(2, Fibonacci.fibonacci(3))

    def test_negative_index_raises_value_error(self) -> None:
        """Дополнительная проверка на отрицательный индекс."""
        with self.assertRaises(ValueError):
            Fibonacci.fibonacci(-1)

    def test_non_integer_index_raises_type_error(self) -> None:
        """Дополнительная проверка на нецелочисленный индекс."""
        with self.assertRaises(TypeError):
            Fibonacci.fibonacci(3.14)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
