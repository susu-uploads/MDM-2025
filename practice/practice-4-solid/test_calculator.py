"""Тесты для консольного калькулятора."""

import unittest

from calculator import Calculator, build_calculator
from main import evaluate_for_output


class CalculatorOutputTests(unittest.TestCase):
    """Проверяет пользовательский вывод калькулятора."""

    calculator: Calculator

    def setUp(self) -> None:
        """Инициализирует калькулятор перед каждым тестом."""
        self.calculator = build_calculator()

    def test_addition(self) -> None:
        """Проверяет сложение."""
        self.assertEqual(evaluate_for_output(self.calculator, "1+1"), "2")

    def test_invalid_input(self) -> None:
        """Проверяет сообщение о неверном формате выражения."""
        self.assertEqual(
            evaluate_for_output(self.calculator, "1а1"),
            "Сообщение: «Ошибка ввода!»",
        )

    def test_division_by_zero(self) -> None:
        """Проверяет сообщение о делении на ноль."""
        self.assertEqual(
            evaluate_for_output(self.calculator, "5/0"),
            "Сообщение: «Невозможно выполнить деление на ноль!»",
        )

    def test_negative_sqrt(self) -> None:
        """Проверяет сообщение о корне из отрицательного числа."""
        self.assertEqual(
            evaluate_for_output(self.calculator, "sqrt(-25)"),
            "Сообщение: «Невозможно выполнить извлечение квадратного корня из отрицательного числа!»",
        )

    def test_square(self) -> None:
        """Проверяет возведение в квадрат."""
        self.assertEqual(evaluate_for_output(self.calculator, "sqr(3)"), "9")

    def test_division(self) -> None:
        """Проверяет деление."""
        self.assertEqual(evaluate_for_output(self.calculator, "9/3"), "3")


if __name__ == "__main__":
    unittest.main()
