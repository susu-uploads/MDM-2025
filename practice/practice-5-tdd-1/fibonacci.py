"""Реализация чисел Фибоначчи для практики TDD-1.

Модуль повторяет структуру из методички на C#:
- класс `Fibonacci`;
- статический метод `Fibonacci(n)` в варианте Python: `fibonacci(n)`.
"""

from __future__ import annotations


class Fibonacci:
    """Класс для вычисления чисел Фибоначчи."""

    @staticmethod
    def fibonacci(n: int) -> int:
        """Возвращает число Фибоначчи по индексу ``n``.

        Реализация повторяет итоговую логику из методички:
        базовые случаи ``0`` и ``1`` и рекурсивная формула для больших значений.

        Args:
            n: Индекс числа Фибоначчи (с нуля).

        Returns:
            Значение числа Фибоначчи с индексом ``n``.

        Raises:
            TypeError: Если ``n`` не является целым числом.
            ValueError: Если ``n`` отрицательное.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("n должен быть целым числом")
        if n < 0:
            raise ValueError("n должен быть больше или равен 0")

        if n == 0:
            return 0
        if n == 1:
            return 1
        return Fibonacci.fibonacci(n - 1) + Fibonacci.fibonacci(n - 2)
