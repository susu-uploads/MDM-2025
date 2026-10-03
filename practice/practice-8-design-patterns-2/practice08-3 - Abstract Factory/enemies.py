"""Иерархия врагов для демонстрации Abstract Factory."""

from __future__ import annotations

from abc import ABC, abstractmethod

from difficulty_level import DifficultyLevel


class Enemy(ABC):
    """Базовая сущность врага."""

    def __init__(self, name: str | None = None) -> None:
        """Создает врага с именем, переданным в конструктор.

        Args:
            name: Имя врага. Если не задано, используется имя класса.
        """
        default_name = self.__class__.__name__
        self.name = name if name is not None else default_name

    @property
    def name(self) -> str:
        """Возвращает имя врага."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя врага с валидацией."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name не должен быть пустым")
        self._name = cleaned

    @property
    @abstractmethod
    def power(self) -> int:
        """Условная сила врага."""
        ...

    @property
    @abstractmethod
    def difficulty(self) -> DifficultyLevel:
        """Уровень сложности, которому соответствует враг."""
        ...

    def __str__(self) -> str:
        """Стандартное строковое представление врага."""
        return (
            f"{self.__class__.__name__}(name={self.name}, power={self.power}, "
            f"difficulty={self.difficulty.value})"
        )


class Soldier(Enemy):
    """Маркерный базовый класс типа Soldier."""


class Monster(Enemy):
    """Маркерный базовый класс типа Monster."""


class SuperMonster(Enemy):
    """Маркерный базовый класс типа SuperMonster."""


class SillySoldier(Soldier):
    """Слабый солдат для легкого уровня."""

    @property
    def power(self) -> int:
        return 10

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.EASY


class SillyMonster(Monster):
    """Слабый монстр для легкого уровня."""

    @property
    def power(self) -> int:
        return 20

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.EASY


class SillySuperMonster(SuperMonster):
    """Слабый супермонстр для легкого уровня."""

    @property
    def power(self) -> int:
        return 35

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.EASY


class BadSoldier(Soldier):
    """Сильный солдат для сложного уровня."""

    @property
    def power(self) -> int:
        return 45

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.HARD


class BadMonster(Monster):
    """Сильный монстр для сложного уровня."""

    @property
    def power(self) -> int:
        return 70

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.HARD


class BadSuperMonster(SuperMonster):
    """Сильный супермонстр для сложного уровня."""

    @property
    def power(self) -> int:
        return 110

    @property
    def difficulty(self) -> DifficultyLevel:
        return DifficultyLevel.HARD
