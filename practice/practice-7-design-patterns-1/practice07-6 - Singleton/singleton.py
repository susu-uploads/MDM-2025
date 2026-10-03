"""Реализация паттерна Singleton на Python."""

from __future__ import annotations

from typing import ClassVar, final


@final
class Singleton:
    """Класс, допускающий существование только одного экземпляра.

    Реализация отражает шаги из методички:
    1. Нельзя создавать объект через прямой вызов конструктора.
    2. Нельзя наследоваться (аналог `sealed` в C#).
    3. Экземпляр создаётся лениво при первом вызове `get_instance`.
    """

    _instance: ClassVar[Singleton | None] = None
    _allow_instantiation: ClassVar[bool] = False

    def __new__(cls) -> Singleton:
        """Контролирует создание экземпляра класса.

        Raises:
            RuntimeError: Если была попытка создать объект напрямую.
        """
        if not cls._allow_instantiation:
            raise RuntimeError("Используйте Singleton.get_instance(), а не Singleton()")

        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance

        return cls._instance

    def __init__(self) -> None:
        """Инициализирует singleton-объект один раз."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.flag: bool = False
        self._initialized = True

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Запрещает наследование от Singleton.

        Raises:
            TypeError: Для любой попытки объявить наследника.
        """
        raise TypeError("Наследование от Singleton запрещено")

    @staticmethod
    def get_instance() -> Singleton:
        """Возвращает единственный экземпляр `Singleton`."""
        if Singleton._instance is None:
            Singleton._allow_instantiation = True
            try:
                Singleton()
            finally:
                Singleton._allow_instantiation = False
        assert Singleton._instance is not None
        return Singleton._instance
