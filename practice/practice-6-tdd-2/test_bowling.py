"""Unit-тесты для практики 6 (TDD-2, однобросковый боулинг)."""

from __future__ import annotations

import unittest

from bowling import Frame, Game


class TestFrame(unittest.TestCase):
    """Проверяет базовое поведение класса Frame."""

    def test_score_no_throws(self) -> None:
        """Пустой фрейм должен иметь 0 очков."""
        frame = Frame()
        self.assertEqual(0, frame.score)

    def test_add_one_throw(self) -> None:
        """Один бросок увеличивает счет фрейма."""
        frame = Frame()
        frame.add(5)
        self.assertEqual(5, frame.score)


class TestGame(unittest.TestCase):
    """Проверяет подсчет очков и логику текущего фрейма в игре."""

    def setUp(self) -> None:
        self.game = Game()

    def _add_many(self, *throws: int) -> None:
        """Утилита добавления последовательности бросков в игру."""
        for pins in throws:
            self.game.add(pins)

    def test_one_throw(self) -> None:
        """После одного броска счет и текущий фрейм соответствуют методичке."""
        self._add_many(5)
        self.assertEqual(5, self.game.get_score())
        self.assertEqual(1, self.game.get_current_frame())

    def test_two_throws_no_mark(self) -> None:
        """Два броска без mark завершают первый фрейм."""
        self._add_many(5, 4)
        self.assertEqual(9, self.game.get_score())
        self.assertEqual(2, self.game.get_current_frame())

    def test_four_throws_no_mark(self) -> None:
        """Проверяет накопленные очки для первых двух фреймов."""
        self._add_many(5, 4, 7, 2)
        self.assertEqual(18, self.game.get_score())
        self.assertEqual(9, self.game.get_score_for_frame(1))
        self.assertEqual(18, self.game.get_score_for_frame(2))
        self.assertEqual(3, self.game.get_current_frame())

    def test_simple_spare(self) -> None:
        """Спэа дает бонус одного следующего броска."""
        self._add_many(3, 7, 3)
        self.assertEqual(13, self.game.get_score_for_frame(1))
        self.assertEqual(2, self.game.get_current_frame())

    def test_simple_frame_after_spare(self) -> None:
        """Проверяет счет после спэа и следующего обычного фрейма."""
        self._add_many(3, 7, 3, 2)
        self.assertEqual(13, self.game.get_score_for_frame(1))
        self.assertEqual(18, self.game.get_score_for_frame(2))
        self.assertEqual(18, self.game.get_score())
        self.assertEqual(3, self.game.get_current_frame())

    def test_simple_strike(self) -> None:
        """Страйк дает бонус двух следующих бросков."""
        self._add_many(10, 3, 6)
        self.assertEqual(19, self.game.get_score_for_frame(1))
        self.assertEqual(28, self.game.get_score())

    def test_tenth_frame_spare_bonus(self) -> None:
        """В 10-м фрейме после спэа доступен один бонусный бросок."""
        self._add_many(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 3, 5)
        self.assertEqual(15, self.game.get_score())

    def test_tenth_frame_strike_bonus(self) -> None:
        """В 10-м фрейме после страйка доступны два бонусных броска."""
        self._add_many(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 4)
        self.assertEqual(17, self.game.get_score())

    def test_sample_card_from_methodical_image(self) -> None:
        """Проверяет последовательность из карточки методички (итог 133)."""
        self._add_many(1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6)
        expected_totals = [5, 14, 29, 49, 60, 61, 77, 97, 117, 133]
        for frame_index, expected in enumerate(expected_totals, start=1):
            self.assertEqual(expected, self.game.get_score_for_frame(frame_index))
        self.assertEqual(133, self.game.get_score())

    def test_perfect_game(self) -> None:
        """12 страйков подряд дают максимум 300 очков."""
        self._add_many(*([10] * 12))
        self.assertEqual(300, self.game.get_score())

    def test_cannot_add_throw_after_finish(self) -> None:
        """После завершения игры новые броски запрещены."""
        self._add_many(*([0] * 20))
        with self.assertRaises(ValueError):
            self.game.add(1)


if __name__ == "__main__":
    unittest.main()
