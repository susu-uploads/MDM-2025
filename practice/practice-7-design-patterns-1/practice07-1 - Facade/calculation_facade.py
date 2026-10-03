"""Реализация паттерна Facade для расчета страховых взносов.

Модуль предоставляет:
- объект `Estate` для передачи входных данных;
- отдельные классы-подсистемы расчета для типов недвижимости;
- фасад `CalculationFacade` как единую точку доступа для клиента.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class EstateType(Enum):
    """Тип недвижимости."""

    APARTMENT = "apartment"
    HOUSE_WITH_LAND = "house_with_land"


class ValueGroup(Enum):
    """Стоимостная группа недвижимости."""

    ECONOMY = "economy"
    COMFORT = "comfort"
    PREMIUM = "premium"


@dataclass(frozen=True)
class Estate:
    """Входные данные для расчета страхового взноса.

    Attributes:
        estate_type: Тип недвижимости.
        area_m2: Площадь в квадратных метрах.
        cadastral_value: Кадастровая стоимость.
        residents_count: Количество проживающих.
        value_group: Стоимостная группа.
    """

    estate_type: EstateType
    area_m2: float
    cadastral_value: float
    residents_count: int
    value_group: ValueGroup

    def __post_init__(self) -> None:
        """Проверяет корректность входных данных."""
        if self.area_m2 <= 0:
            raise ValueError("area_m2 должен быть больше 0")
        if self.cadastral_value < 0:
            raise ValueError("cadastral_value не может быть отрицательным")
        if isinstance(self.residents_count, bool) or self.residents_count < 1:
            raise ValueError("residents_count должен быть >= 1")


class ContributionCalculator(ABC):
    """Интерфейс подсистемы расчета страхового взноса."""

    @abstractmethod
    def calculate(self, estate: Estate) -> float:
        """Вычисляет страховой взнос для переданного объекта `Estate`."""
        ...


class ApartmentContributionCalculator(ContributionCalculator):
    """Подсистема расчета взноса для квартиры."""

    _BASE_RATE_PER_M2: float = 8.0
    _VALUE_GROUP_COEFFICIENTS: dict[ValueGroup, float] = {
        ValueGroup.ECONOMY: 1.0,
        ValueGroup.COMFORT: 1.2,
        ValueGroup.PREMIUM: 1.45,
    }
    _EXTRA_RESIDENT_COEFFICIENT: float = 0.02

    def calculate(self, estate: Estate) -> float:
        """Вычисляет взнос для квартиры."""
        base = estate.area_m2 * self._BASE_RATE_PER_M2
        group_coef = self._VALUE_GROUP_COEFFICIENTS[estate.value_group]
        residents_coef = 1.0 + max(estate.residents_count - 1, 0) * self._EXTRA_RESIDENT_COEFFICIENT
        return round(base * group_coef * residents_coef, 2)


class HouseWithLandContributionCalculator(ContributionCalculator):
    """Подсистема расчета взноса для дома с земельным участком."""

    _BUILDING_RATE_PER_M2: float = 6.5
    _LAND_RATE_FROM_CADASTRAL: float = 0.0015
    _PER_RESIDENT_FIXED_FEE: float = 25.0
    _VALUE_GROUP_COEFFICIENTS: dict[ValueGroup, float] = {
        ValueGroup.ECONOMY: 1.05,
        ValueGroup.COMFORT: 1.2,
        ValueGroup.PREMIUM: 1.35,
    }

    def calculate(self, estate: Estate) -> float:
        """Вычисляет взнос для дома с земельным участком."""
        building_part = estate.area_m2 * self._BUILDING_RATE_PER_M2
        land_part = estate.cadastral_value * self._LAND_RATE_FROM_CADASTRAL
        residents_part = estate.residents_count * self._PER_RESIDENT_FIXED_FEE
        group_coef = self._VALUE_GROUP_COEFFICIENTS[estate.value_group]
        return round((building_part + land_part + residents_part) * group_coef, 2)


class CalculationFacade:
    """Фасад для расчета страховых взносов по объекту `Estate`.

    Клиент взаимодействует только с этим классом, а конкретные алгоритмы
    расчета можно подменять через `register_calculator`.
    """

    def __init__(self) -> None:
        """Создает фасад со стандартными подсистемами расчета."""
        self._calculators: dict[EstateType, ContributionCalculator] = {
            EstateType.APARTMENT: ApartmentContributionCalculator(),
            EstateType.HOUSE_WITH_LAND: HouseWithLandContributionCalculator(),
        }

    def register_calculator(self, estate_type: EstateType, calculator: ContributionCalculator) -> None:
        """Регистрирует/заменяет подсистему расчета для типа недвижимости."""
        self._calculators[estate_type] = calculator

    def calculate_contribution(self, estate: Estate) -> float:
        """Рассчитывает страховой взнос через соответствующую подсистему."""
        calculator = self._calculators.get(estate.estate_type)
        if calculator is None:
            raise ValueError(f"Нет калькулятора для типа недвижимости: {estate.estate_type.value}")
        return calculator.calculate(estate)
