"""Сущности фильмов для приложения «Кинопрокат»."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MovieType(Enum):
    """Тип фильма, влияющий на правила расчета аренды."""

    REGULAR = "regular"
    NEW_RELEASE = "new_release"
    CHILDREN = "children"


@dataclass(frozen=True)
class Movie:
    """Фильм в каталоге проката.

    Attributes:
        title: Название фильма.
        movie_type: Тип фильма для тарифной политики.
    """

    title: str
    movie_type: MovieType

    def __post_init__(self) -> None:
        """Проверяет корректность названия фильма."""
        if not self.title.strip():
            raise ValueError("title не должен быть пустым")
