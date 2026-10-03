"""Unit-тесты для варианта Adapter."""

from __future__ import annotations

import unittest

from adapter import SecureBlackboxSSHTunnelAdapter
from ssh_client import ElSimpleSSHClient
from ssh_tunnel import SSHTunnel


def open_and_close_tunnel(tunnel: SSHTunnel) -> bool:
    """Клиентский сценарий, завязанный только на интерфейс `SSHTunnel`."""
    tunnel.open()
    tunnel.close()
    return True


class InspectableAdapter(SecureBlackboxSSHTunnelAdapter):
    """Тестовый наследник, открывающий доступ к внутреннему клиенту только в тестах."""

    @property
    def test_client(self) -> ElSimpleSSHClient:
        """Возвращает внутренний адаптируемый клиент для проверок тестов."""
        return self._ssh_client


class TestSecureBlackboxSSHTunnelAdapter(unittest.TestCase):
    """Проверяет корректность адаптации стороннего SSH-клиента."""

    def setUp(self) -> None:
        self.adapter = InspectableAdapter()

    def test_internal_socket_enabled_in_constructor(self) -> None:
        """Адаптер должен включать use_internal_socket при создании."""
        self.assertTrue(self.adapter.test_client.use_internal_socket)

    def test_local_port_mapping(self) -> None:
        """Проверяет маппинг local_port <-> bind_port внешнего клиента."""
        self.adapter.local_port = 50022
        self.assertEqual(50022, self.adapter.local_port)
        self.assertEqual(50022, self.adapter.test_client.bind_port)

    def test_remote_host_mapping(self) -> None:
        """Проверяет маппинг remote_host <-> destination_host."""
        self.adapter.remote_host = "example.org"
        self.assertEqual("example.org", self.adapter.remote_host)
        self.assertEqual("example.org", self.adapter.test_client.destination_host)

    def test_remote_port_mapping(self) -> None:
        """Проверяет маппинг remote_port <-> destination_port."""
        self.adapter.remote_port = 22
        self.assertEqual(22, self.adapter.remote_port)
        self.assertEqual(22, self.adapter.test_client.destination_port)

    def test_adapter_works_via_interface(self) -> None:
        """Клиентский код должен работать через абстракцию `SSHTunnel`."""
        self.assertTrue(open_and_close_tunnel(self.adapter))

    def test_local_port_validation(self) -> None:
        """Проверяет валидацию local_port."""
        with self.assertRaises(ValueError):
            self.adapter.local_port = 0
        with self.assertRaises(ValueError):
            self.adapter.local_port = 70000
        with self.assertRaises(TypeError):
            self.adapter.local_port = "22"  # type: ignore[assignment]

    def test_remote_port_validation(self) -> None:
        """Проверяет валидацию remote_port."""
        with self.assertRaises(ValueError):
            self.adapter.remote_port = 0
        with self.assertRaises(ValueError):
            self.adapter.remote_port = 70000
        with self.assertRaises(TypeError):
            self.adapter.remote_port = 22.5  # type: ignore[assignment]

    def test_remote_host_validation(self) -> None:
        """Проверяет валидацию remote_host."""
        with self.assertRaises(ValueError):
            self.adapter.remote_host = "   "
        with self.assertRaises(TypeError):
            self.adapter.remote_host = 123  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
