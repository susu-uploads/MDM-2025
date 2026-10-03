"""Объявление уровней сложности для модуля врагов."""

from __future__ import annotations

from enum import Enum


class DifficultyLevel(Enum):
    """Уровень сложности игры."""

    EASY = "easy"
    HARD = "hard"
