"""Фабрики создания врагов для паттерна Abstract Factory."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping, TypeVar, cast

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

TEnemy = TypeVar("TEnemy", bound=Enemy)


class AbstractEnemyFactory(ABC):
    """Абстрактная фабрика создания врагов."""

    @property
    @abstractmethod
    def registry(self) -> Mapping[type[Enemy], type[Enemy]]:
        """Отображение маркерного типа врага в конкретный класс реализации."""
        ...

    def create(self, enemy_type: type[TEnemy], *, name: str | None = None) -> TEnemy:
        """Создает врага указанного маркерного типа.

        Args:
            enemy_type: Один из типов `Soldier`, `Monster`, `SuperMonster`.
            name: Имя врага, передаваемое в конструктор.

        Returns:
            Экземпляр конкретного класса врага для данной фабрики.
        """
        enemy_cls = self.registry.get(enemy_type)
        if enemy_cls is None:
            raise ValueError(f"Тип врага не поддерживается: {enemy_type.__name__}")
        return cast(TEnemy, enemy_cls(name=name))

    def make_soldier(self) -> Soldier:
        """Создает врага типа Soldier."""
        return self.create(Soldier)

    def make_monster(self) -> Monster:
        """Создает врага типа Monster."""
        return self.create(Monster)

    def make_super_monster(self) -> SuperMonster:
        """Создает врага типа SuperMonster."""
        return self.create(SuperMonster)


class EasyLevelEnemyFactory(AbstractEnemyFactory):
    """Фабрика врагов для легкого уровня сложности."""

    _registry: Mapping[type[Enemy], type[Enemy]] = {
        Soldier: SillySoldier,
        Monster: SillyMonster,
        SuperMonster: SillySuperMonster,
    }

    @property
    def registry(self) -> Mapping[type[Enemy], type[Enemy]]:
        return self._registry


class HardLevelEnemyFactory(AbstractEnemyFactory):
    """Фабрика врагов для сложного уровня сложности."""

    _registry: Mapping[type[Enemy], type[Enemy]] = {
        Soldier: BadSoldier,
        Monster: BadMonster,
        SuperMonster: BadSuperMonster,
    }

    @property
    def registry(self) -> Mapping[type[Enemy], type[Enemy]]:
        return self._registry


def create_factory(level: DifficultyLevel) -> AbstractEnemyFactory:
    """Создает фабрику врагов под выбранный уровень сложности."""
    if level is DifficultyLevel.EASY:
        return EasyLevelEnemyFactory()
    if level is DifficultyLevel.HARD:
        return HardLevelEnemyFactory()
    raise ValueError(f"Неподдерживаемый уровень сложности: {level}")


def make_named_enemy(factory: AbstractEnemyFactory, enemy_type: type[TEnemy], name: str) -> TEnemy:
    """Обобщенная функция создания именованного врага."""
    return factory.create(enemy_type, name=name)
