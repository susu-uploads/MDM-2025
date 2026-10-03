"""Unit-тесты для практики 8-1 (паттерн Facade)."""

from __future__ import annotations

import unittest

from calculation_facade import (
    CalculationFacade,
    ContributionCalculator,
    Estate,
    EstateType,
    ValueGroup,
)


class FixedContributionCalculator(ContributionCalculator):
    """Тестовый калькулятор с фиксированным результатом."""

    def __init__(self, fixed_value: float) -> None:
        self._fixed_value = fixed_value

    def calculate(self, estate: Estate) -> float:
        return self._fixed_value


class TestCalculationFacade(unittest.TestCase):
    """Проверяет корректность работы фасада и подсистем расчета."""

    def test_apartment_contribution(self) -> None:
        """Проверяет расчет взноса для квартиры."""
        estate = Estate(
            estate_type=EstateType.APARTMENT,
            area_m2=60,
            cadastral_value=5_000_000,
            residents_count=3,
            value_group=ValueGroup.COMFORT,
        )
        amount = CalculationFacade().calculate_contribution(estate)
        self.assertAlmostEqual(599.04, amount, places=2)

    def test_house_with_land_contribution(self) -> None:
        """Проверяет расчет взноса для дома с участком."""
        estate = Estate(
            estate_type=EstateType.HOUSE_WITH_LAND,
            area_m2=140,
            cadastral_value=12_000_000,
            residents_count=4,
            value_group=ValueGroup.PREMIUM,
        )
        amount = CalculationFacade().calculate_contribution(estate)
        self.assertAlmostEqual(25_663.50, amount, places=2)

    def test_register_custom_calculator(self) -> None:
        """Проверяет подмену алгоритма через фасад."""
        facade = CalculationFacade()
        facade.register_calculator(EstateType.APARTMENT, FixedContributionCalculator(42.0))

        estate = Estate(
            estate_type=EstateType.APARTMENT,
            area_m2=45,
            cadastral_value=4_500_000,
            residents_count=2,
            value_group=ValueGroup.ECONOMY,
        )
        self.assertEqual(42.0, facade.calculate_contribution(estate))

    def test_error_when_calculator_missing(self) -> None:
        """Проверяет ошибку при отсутствии калькулятора для типа недвижимости."""
        facade = CalculationFacade()
        facade._calculators.pop(EstateType.APARTMENT)

        estate = Estate(
            estate_type=EstateType.APARTMENT,
            area_m2=50,
            cadastral_value=4_000_000,
            residents_count=2,
            value_group=ValueGroup.COMFORT,
        )

        with self.assertRaises(ValueError):
            facade.calculate_contribution(estate)

    def test_estate_validation(self) -> None:
        """Проверяет валидацию входных параметров `Estate`."""
        with self.assertRaises(ValueError):
            Estate(
                estate_type=EstateType.APARTMENT,
                area_m2=-1,
                cadastral_value=1_000_000,
                residents_count=1,
                value_group=ValueGroup.ECONOMY,
            )

        with self.assertRaises(ValueError):
            Estate(
                estate_type=EstateType.APARTMENT,
                area_m2=30,
                cadastral_value=-1,
                residents_count=1,
                value_group=ValueGroup.ECONOMY,
            )

        with self.assertRaises(ValueError):
            Estate(
                estate_type=EstateType.APARTMENT,
                area_m2=30,
                cadastral_value=1_000_000,
                residents_count=0,
                value_group=ValueGroup.ECONOMY,
            )


if __name__ == "__main__":
    unittest.main()
