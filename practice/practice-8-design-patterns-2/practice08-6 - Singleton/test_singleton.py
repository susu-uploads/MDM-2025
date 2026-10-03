"""Unit-тесты для реализации паттерна Singleton."""

from __future__ import annotations

import importlib
import unittest
from types import ModuleType


def load_fresh_singleton_module() -> ModuleType:
    """Перезагружает модуль `singleton` для изоляции тестов."""
    module = importlib.import_module("singleton")
    return importlib.reload(module)


class TestSingleton(unittest.TestCase):
    """Проверяет функциональность и ограничения Singleton."""

    def test_get_instance_returns_same_object(self) -> None:
        """Повторные вызовы `get_instance` должны возвращать один объект."""
        module = load_fresh_singleton_module()
        singleton_1 = module.Singleton.get_instance()
        singleton_2 = module.Singleton.get_instance()
        self.assertIs(singleton_1, singleton_2)

    def test_flag_change_visible_through_second_reference(self) -> None:
        """Изменение поля через одну ссылку видно через другую ссылку."""
        module = load_fresh_singleton_module()
        single_object = module.Singleton.get_instance()
        single_object.flag = True

        single_object1 = module.Singleton.get_instance()
        single_object1.flag = False

        self.assertFalse(single_object.flag)

    def test_direct_constructor_call_forbidden(self) -> None:
        """Прямой вызов конструктора должен завершаться ошибкой."""
        module = load_fresh_singleton_module()
        with self.assertRaises(RuntimeError):
            module.Singleton()

    def test_singleton_inheritance_forbidden(self) -> None:
        """Проверяет запрет наследования (аналог sealed)."""
        module = load_fresh_singleton_module()
        with self.assertRaises(TypeError):
            class ChildSingleton(module.Singleton):
                pass

if __name__ == "__main__":
    unittest.main()
