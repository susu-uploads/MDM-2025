"""Unit-тесты для варианта Strategy (Кинопрокат)."""

from __future__ import annotations

import unittest
from unittest.mock import Mock

from customer import Customer
from movie import Movie, MovieType
from rental import Rental
from statements import HTMLStatement, Statement, TextStatement


def build_customer_fixture() -> Customer:
    """Создает тестового арендатора с несколькими арендами."""
    customer = Customer(name="Иван")
    customer.add_rental(Rental(movie=Movie("Матрица", MovieType.NEW_RELEASE), days_rented=3))
    customer.add_rental(Rental(movie=Movie("Терминатор", MovieType.REGULAR), days_rented=1))
    customer.add_rental(Rental(movie=Movie("История игрушек", MovieType.CHILDREN), days_rented=4))
    return customer


class TestStrategyMovieRental(unittest.TestCase):
    """Проверяет формирование отчетов и расчеты задолженности/баллов."""

    def test_customer_delegates_to_statement_strategy(self) -> None:
        """Проверяет, что Customer делегирует отчёт в Statement.get_value."""
        customer = build_customer_fixture()
        statement = Mock(spec=Statement)
        statement.get_value.return_value = "delegated result"

        value = customer.get_statement_value(statement)

        self.assertEqual("delegated result", value)
        statement.get_value.assert_called_once_with(customer)

    def test_total_charge(self) -> None:
        """Проверяет итоговую сумму задолженности арендатора."""
        customer = build_customer_fixture()
        self.assertAlmostEqual(14.0, customer.get_total_charge(), places=2)

    def test_total_frequent_renter_points(self) -> None:
        """Проверяет итоговые баллы за активность."""
        customer = build_customer_fixture()
        self.assertEqual(4, customer.get_total_frequent_renter_points())

    def test_text_statement(self) -> None:
        """Проверяет формат текстового отчета."""
        customer = build_customer_fixture()
        value = customer.get_statement_value(TextStatement())
        expected = (
            "Учёт аренды для Иван\n"
            "\tМатрица\t9\n"
            "\tТерминатор\t2\n"
            "\tИстория игрушек\t3\n"
            "Сумма задолженности составляет 14\n"
            "Сумма очков за активность составляет 4"
        )
        self.assertEqual(expected, value)

    def test_html_statement(self) -> None:
        """Проверяет формат HTML-отчета."""
        customer = build_customer_fixture()
        value = customer.get_statement_value(HTMLStatement())
        expected = (
            "<H1>Учёт аренды для <EM>Иван</EM></H1><P>"
            "Матрица\t9<BR>"
            "Терминатор\t2<BR>"
            "История игрушек\t3<BR>"
            "<P>Сумма задолженности составляет <EM>14</EM><BR>"
            "<P>Сумма очков за активность составляет <EM>4</EM>"
        )
        self.assertEqual(expected, value)

    def test_strategy_switch(self) -> None:
        """Проверяет, что разные стратегии дают разный формат отчета."""
        customer = build_customer_fixture()
        text_value = customer.get_statement_value(TextStatement())
        html_value = customer.get_statement_value(HTMLStatement())
        self.assertNotEqual(text_value, html_value)

    def test_new_release_bonus_points(self) -> None:
        """Проверяет бонусные баллы для new_release при аренде более 1 дня."""
        customer = Customer(name="Петр")
        customer.add_rental(Rental(movie=Movie("Дюна", MovieType.NEW_RELEASE), days_rented=2))
        self.assertEqual(2, customer.get_total_frequent_renter_points())


if __name__ == "__main__":
    unittest.main()
