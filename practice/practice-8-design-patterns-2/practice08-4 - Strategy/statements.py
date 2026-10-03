"""Стратегии формирования отчетов в приложении «Кинопрокат»."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from rental import Rental

if TYPE_CHECKING:
    from customer import Customer


def format_amount(value: float) -> str:
    """Форматирует сумму без лишних нулей после запятой."""
    as_int = int(value)
    if value == as_int:
        return str(as_int)
    return f"{value:.2f}".rstrip("0").rstrip(".")


class Statement(ABC):
    """Базовая стратегия форматирования отчета по арендам.

    Метод `get_value` реализует шаблон общего алгоритма:
    1. Заголовок.
    2. Строки по каждой аренде.
    3. Подвал с итогами.
    """

    def get_value(self, customer: Customer) -> str:
        """Формирует итоговый отчет по арендатору."""
        result = self.get_header(customer)
        for rental in customer.rentals:
            result += self.get_rental_string(rental)
        result += self.get_footer(customer)
        return result

    @abstractmethod
    def get_footer(self, customer: Customer) -> str:
        """Возвращает подвал отчета."""
        ...

    @abstractmethod
    def get_rental_string(self, rental: Rental) -> str:
        """Возвращает строку отчета по одной аренде."""
        ...

    @abstractmethod
    def get_header(self, customer: Customer) -> str:
        """Возвращает заголовок отчета."""
        ...


class TextStatement(Statement):
    """Стратегия отчета в текстовом формате."""

    def get_header(self, customer: Customer) -> str:
        return f"Учёт аренды для {customer.name}\n"

    def get_rental_string(self, rental: Rental) -> str:
        return f"\t{rental.movie.title}\t{format_amount(rental.charge)}\n"

    def get_footer(self, customer: Customer) -> str:
        return (
            f"Сумма задолженности составляет {format_amount(customer.get_total_charge())}\n"
            f"Сумма очков за активность составляет {customer.get_total_frequent_renter_points()}"
        )


class HTMLStatement(Statement):
    """Стратегия отчета в HTML-формате."""

    def get_header(self, customer: Customer) -> str:
        return f"<H1>Учёт аренды для <EM>{customer.name}</EM></H1><P>"

    def get_rental_string(self, rental: Rental) -> str:
        return f"{rental.movie.title}\t{format_amount(rental.charge)}<BR>"

    def get_footer(self, customer: Customer) -> str:
        return (
            f"<P>Сумма задолженности составляет <EM>{format_amount(customer.get_total_charge())}</EM><BR>"
            f"<P>Сумма очков за активность составляет <EM>{customer.get_total_frequent_renter_points()}</EM>"
        )
