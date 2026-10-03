"""Сущность аренды фильма с делегированием тарифных расчётов."""

from __future__ import annotations

from dataclasses import dataclass

from movie import Movie
from pricing import get_price_policy


@dataclass(frozen=True)
class Rental:
    """Факт аренды конкретного фильма.

    Attributes:
        movie: Взятый в аренду фильм.
        days_rented: Количество дней аренды.
    """

    movie: Movie
    days_rented: int

    def __post_init__(self) -> None:
        """Проверяет корректность срока аренды."""
        if isinstance(self.days_rented, bool) or self.days_rented <= 0:
            raise ValueError("days_rented должен быть больше 0")

    @property
    def charge(self) -> float:
        """Сумма аренды, рассчитанная тарифной политикой фильма."""
        policy = get_price_policy(self.movie.movie_type)
        return policy.calculate_charge(self.days_rented)

    @property
    def frequent_renter_points(self) -> int:
        """Баллы за активность, рассчитанные тарифной политикой фильма."""
        policy = get_price_policy(self.movie.movie_type)
        return policy.calculate_frequent_renter_points(self.days_rented)
