"""Модель арендатора и агрегирование данных по арендованным фильмам."""

from __future__ import annotations

from dataclasses import dataclass, field

from rental import Rental
from statements import Statement


@dataclass
class Customer:
    """Арендатор в приложении «Кинопрокат»."""

    name: str
    rentals: list[Rental] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Проверяет корректность имени арендатора."""
        if not self.name.strip():
            raise ValueError("name не должен быть пустым")

    def add_rental(self, rental: Rental) -> None:
        """Добавляет факт аренды в список арендатора."""
        self.rentals.append(rental)

    def get_total_charge(self) -> float:
        """Возвращает общую сумму задолженности по всем арендам."""
        return sum(item.charge for item in self.rentals)

    def get_total_frequent_renter_points(self) -> int:
        """Возвращает суммарные баллы за активность."""
        return sum(item.frequent_renter_points for item in self.rentals)

    def get_statement_value(self, statement: Statement) -> str:
        """Делегирует формирование отчета стратегии `Statement`."""
        return statement.get_value(self)
