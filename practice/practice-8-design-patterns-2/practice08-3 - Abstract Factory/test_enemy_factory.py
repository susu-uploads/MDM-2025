"""Unit-тесты для варианта Abstract Factory."""

from __future__ import annotations

import unittest

from difficulty_level import DifficultyLevel
from enemies import (
    BadMonster,
    BadSoldier,
    BadSuperMonster,
    Enemy,
    Monster,
    SillyMonster,
    SillySoldier,
    SillySuperMonster,
    Soldier,
    SuperMonster,
)
from enemy_factory import (
    HardLevelEnemyFactory,
    EasyLevelEnemyFactory,
    create_factory,
    make_named_enemy,
)


class Boss(Enemy):
    """Тестовый тип врага, которого нет в реестре фабрик."""

    @property
    def power(self) -> int:
        return 999

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.HARD


class TestAbstractFactory(unittest.TestCase):
    """Проверяет создание семейств врагов через фабрики."""

    def test_easy_factory_creates_easy_family(self) -> None:
        """Легкая фабрика должна возвращать Silly-врагов."""
        factory = EasyLevelEnemyFactory()
        self.assertIsInstance(factory.make_soldier(), SillySoldier)
        self.assertIsInstance(factory.make_monster(), SillyMonster)
        self.assertIsInstance(factory.make_super_monster(), SillySuperMonster)

    def test_hard_factory_creates_hard_family(self) -> None:
        """Сложная фабрика должна возвращать Bad-врагов."""
        factory = HardLevelEnemyFactory()
        self.assertIsInstance(factory.make_soldier(), BadSoldier)
        self.assertIsInstance(factory.make_monster(), BadMonster)
        self.assertIsInstance(factory.make_super_monster(), BadSuperMonster)

    def test_generic_create_method(self) -> None:
        """Обобщенный метод create должен работать с маркерными типами."""
        factory = EasyLevelEnemyFactory()
        soldier = factory.create(Soldier)
        monster = factory.create(Monster)
        super_monster = factory.create(SuperMonster)
        self.assertIsInstance(soldier, SillySoldier)
        self.assertIsInstance(monster, SillyMonster)
        self.assertIsInstance(super_monster, SillySuperMonster)

    def test_make_named_enemy(self) -> None:
        """Проверяет обобщенную функцию создания именованного врага."""
        factory = HardLevelEnemyFactory()
        enemy = make_named_enemy(factory, Monster, "Kraken")
        self.assertIsInstance(enemy, BadMonster)
        self.assertEqual("Kraken", enemy.name)

    def test_create_factory_by_level(self) -> None:
        """Функция create_factory должна выбирать корректную фабрику."""
        self.assertIsInstance(create_factory(DifficultyLevel.EASY), EasyLevelEnemyFactory)
        self.assertIsInstance(create_factory(DifficultyLevel.HARD), HardLevelEnemyFactory)

    def test_unknown_enemy_type_raises_error(self) -> None:
        """При неизвестном типе врага фабрика должна выбрасывать ошибку."""
        factory = EasyLevelEnemyFactory()
        with self.assertRaises(ValueError):
            factory.create(Boss)

    def test_name_validation(self) -> None:
        """Имя врага не должно быть пустым."""
        factory = EasyLevelEnemyFactory()
        with self.assertRaises(ValueError):
            make_named_enemy(factory, Soldier, "   ")


if __name__ == "__main__":
    unittest.main()
