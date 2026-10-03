"""Стратегии расчёта стоимости аренды и баллов за активность."""

from __future__ import annotations

from abc import ABC, abstractmethod

from movie import MovieType


class PricePolicy(ABC):
    """Абстракция тарифной политики для конкретного типа фильма."""

    @abstractmethod
    def calculate_charge(self, days_rented: int) -> float:
        """Вычисляет сумму аренды по числу дней."""
        ...

    def calculate_frequent_renter_points(self, days_rented: int) -> int:
        """Вычисляет баллы за активность.

        Базовое правило: за любую аренду начисляется 1 балл.
        """
        return 1


class RegularPricePolicy(PricePolicy):
    """Тариф для regular-фильмов."""

    def calculate_charge(self, days_rented: int) -> float:
        """2 + 1.5 за каждый день после второго."""
        amount = 2.0
        if days_rented > 2:
            amount += (days_rented - 2) * 1.5
        return amount


class NewReleasePricePolicy(PricePolicy):
    """Тариф для new_release-фильмов."""

    def calculate_charge(self, days_rented: int) -> float:
        """3 за каждый день аренды."""
        return days_rented * 3.0

    def calculate_frequent_renter_points(self, days_rented: int) -> int:
        """2 балла при аренде более чем на 1 день, иначе 1."""
        if days_rented > 1:
            return 2
        return 1


class ChildrenPricePolicy(PricePolicy):
    """Тариф для children-фильмов."""

    def calculate_charge(self, days_rented: int) -> float:
        """1.5 + 1.5 за каждый день после третьего."""
        amount = 1.5
        if days_rented > 3:
            amount += (days_rented - 3) * 1.5
        return amount


_PRICE_POLICIES: dict[MovieType, PricePolicy] = {
    MovieType.REGULAR: RegularPricePolicy(),
    MovieType.NEW_RELEASE: NewReleasePricePolicy(),
    MovieType.CHILDREN: ChildrenPricePolicy(),
}


def get_price_policy(movie_type: MovieType) -> PricePolicy:
    """Возвращает тарифную политику для указанного типа фильма."""
    try:
        return _PRICE_POLICIES[movie_type]
    except KeyError as error:
        raise ValueError(f"Неизвестный тип фильма: {movie_type}") from error
