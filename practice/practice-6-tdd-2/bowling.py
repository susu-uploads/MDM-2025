"""Доменная модель игры «Однобросковый боулинг».

Модуль нужен для расчета очков по правилам классического боулинга:
- хранит структуру игры через классы `Game`, `Frame`, `Throw`;
- принимает броски по одному;
- вычисляет текущий и покадровый счет с учетом `strike`/`spare`;
- отслеживает завершение игры и номер текущего фрейма.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Throw:
    """Один бросок в боулинге.

    Attributes:
        pins: Количество сбитых кеглей (0..10).
    """

    pins: int

    def __post_init__(self) -> None:
        """Проверяет валидность количества сбитых кеглей."""
        if isinstance(self.pins, bool) or not isinstance(self.pins, int):
            raise TypeError("pins должен быть целым числом")
        if self.pins < 0 or self.pins > 10:
            raise ValueError("pins должен быть в диапазоне 0..10")


class Frame:
    """Фрейм игры, содержащий 2 броска (или до 3 бросков в 10-м фрейме)."""

    def __init__(self, *, is_tenth: bool = False) -> None:
        """Создает фрейм.

        Args:
            is_tenth: Признак десятого фрейма (особые правила бонусных бросков).
        """
        self._is_tenth = is_tenth
        self._throws: list[Throw] = []

    @property
    def is_tenth(self) -> bool:
        """Признак десятого фрейма."""
        return self._is_tenth

    @property
    def throws(self) -> tuple[Throw, ...]:
        """Кортеж бросков, уже совершенных в данном фрейме."""
        return tuple(self._throws)

    @property
    def score(self) -> int:
        """Сумма кеглей, сбитых в самом фрейме (без бонусов следующих фреймов)."""
        return sum(item.pins for item in self._throws)

    @property
    def is_strike(self) -> bool:
        """True, если первым броском во фрейме сбито 10 кеглей."""
        return bool(self._throws) and self._throws[0].pins == 10

    @property
    def is_spare(self) -> bool:
        """True, если за первые два броска во фрейме сбито 10 кеглей."""
        return (
            len(self._throws) >= 2
            and self._throws[0].pins < 10
            and (self._throws[0].pins + self._throws[1].pins) == 10
        )

    @property
    def is_complete(self) -> bool:
        """True, если фрейм завершен по правилам боулинга."""
        if not self._throws:
            return False

        if not self._is_tenth:
            return self.is_strike or len(self._throws) == 2

        # Десятый фрейм.
        if len(self._throws) < 2:
            return False

        first = self._throws[0].pins
        second = self._throws[1].pins

        if first == 10:
            return len(self._throws) == 3
        if first + second == 10:
            return len(self._throws) == 3
        return len(self._throws) == 2

    def add(self, pins: int) -> None:
        """Добавляет бросок во фрейм.

        Args:
            pins: Количество кеглей, сбитых броском.

        Raises:
            ValueError: Если бросок невозможен по правилам текущего состояния фрейма.
            TypeError: Если передан нецелочисленный `pins`.
        """
        if self.is_complete:
            raise ValueError("Фрейм уже завершен")

        throw = Throw(pins)
        self._validate_throw(throw.pins)
        self._throws.append(throw)

    def _validate_throw(self, pins: int) -> None:
        """Проверяет, что бросок допустим в текущем состоянии фрейма."""
        if not self._throws:
            return

        first = self._throws[0].pins

        if not self._is_tenth:
            if len(self._throws) == 1 and first < 10 and (first + pins) > 10:
                raise ValueError("Во фрейме (кроме 10-го) сумма двух бросков не может быть > 10")
            return

        # Правила десятого фрейма.
        if len(self._throws) == 1:
            if first < 10 and (first + pins) > 10:
                raise ValueError("В 10-м фрейме без strike сумма первых двух бросков не может быть > 10")
            return

        if len(self._throws) == 2:
            second = self._throws[1].pins
            if first == 10 and second < 10 and (second + pins) > 10:
                raise ValueError(
                    "В 10-м фрейме после strike и не-strike второго броска третий бросок ограничен остатком до 10"
                )


class Game:
    """Партия боулинга из 10 фреймов с подсчетом очков по классическим правилам."""

    MAX_FRAMES: int = 10

    def __init__(self) -> None:
        """Создает новую игру."""
        self._frames: list[Frame] = []

    @property
    def frames(self) -> tuple[Frame, ...]:
        """Текущий список фреймов (только чтение)."""
        return tuple(self._frames)

    @property
    def is_finished(self) -> bool:
        """True, если игра полностью завершена (10-й фрейм закрыт)."""
        return len(self._frames) == self.MAX_FRAMES and self._frames[-1].is_complete

    def add(self, pins: int) -> None:
        """Добавляет один бросок в текущую игру.

        Args:
            pins: Количество сбитых кеглей за бросок.

        Raises:
            ValueError: Если игра уже завершена.
            ValueError/TypeError: Если нарушены ограничения броска.
        """
        if self.is_finished:
            raise ValueError("Игра уже завершена")

        frame = self._get_or_create_current_frame()
        frame.add(pins)

    def get_score(self) -> int:
        """Возвращает суммарный счет текущей игры на данный момент."""
        return self.get_score_for_frame(len(self._frames))

    def get_score_for_frame(self, frame_number: int) -> int:
        """Возвращает накопленный счет до указанного номера фрейма (включительно).

        Args:
            frame_number: Количество первых фреймов, для которых нужен итог.

        Returns:
            Накопленный счет.

        Raises:
            ValueError: Если `frame_number` вне диапазона доступных фреймов.
        """
        if frame_number < 0 or frame_number > len(self._frames):
            raise ValueError("frame_number вне диапазона сыгранных фреймов")

        total = 0
        for index in range(frame_number):
            total += self._score_of_frame(index)
        return total

    def get_current_frame(self) -> int:
        """Возвращает номер текущего фрейма (куда пойдет следующий бросок).

        Returns:
            Номер фрейма от 1 до 11.
            Значение 11 означает, что игра завершена.
        """
        if not self._frames:
            return 1
        if self.is_finished:
            return 11
        if self._frames[-1].is_complete:
            return len(self._frames) + 1
        return len(self._frames)

    def _get_or_create_current_frame(self) -> Frame:
        """Возвращает текущий фрейм, создавая новый при необходимости."""
        if not self._frames:
            self._frames.append(Frame())
            return self._frames[-1]

        if self._frames[-1].is_complete and len(self._frames) < self.MAX_FRAMES:
            is_tenth = len(self._frames) == (self.MAX_FRAMES - 1)
            self._frames.append(Frame(is_tenth=is_tenth))

        return self._frames[-1]

    def _score_of_frame(self, index: int) -> int:
        """Возвращает счет конкретного фрейма с учетом бонусов."""
        frame = self._frames[index]

        # 10-й фрейм не использует бонусы из следующих фреймов.
        if index == self.MAX_FRAMES - 1:
            return frame.score

        if frame.is_strike:
            return 10 + sum(self._next_throws(index, 2))

        if frame.is_spare:
            bonus = self._next_throws(index, 1)
            return 10 + (bonus[0] if bonus else 0)

        return frame.score

    def _next_throws(self, index: int, count: int) -> list[int]:
        """Возвращает список следующих `count` бросков после фрейма `index`."""
        pins: list[int] = []
        for frame in self._frames[index + 1 :]:
            pins.extend(item.pins for item in frame.throws)
            if len(pins) >= count:
                break
        return pins[:count]
