# Практика 7-2: Adapter (Python)

Реализован паттерн `Adapter` для совместимости внешнего класса `ElSimpleSSHClient`
с требуемым интерфейсом `SSHTunnel`.

## Что реализовано

- `ssh_tunnel.py`: абстракция `SSHTunnel` (local_port, remote_host, remote_port, open, close).
- `ssh_client.py`: эмуляция стороннего класса `ElSimpleSSHClient`.
- `adapter.py`: `SecureBlackboxSSHTunnelAdapter`, который адаптирует внешний API.
- `main.py`: консольная демонстрация настройки туннеля.
- `test_adapter.py`: unit-тесты адаптера.

## Диаграмма классов

```text
+-------------------------------------+   inherits   +------------------+
| SecureBlackboxSSHTunnelAdapter      | -----------> |    SSHTunnel     |
+-------------------------------------+              +------------------+
                   |
                   | adapts / wraps
                   v
+-------------------------------------+
|          ElSimpleSSHClient          |
+-------------------------------------+
```

## Запуск приложения

```bash
python3 main.py
```

Введите одну строку в формате:

`local_port remote_host remote_port`

Пример:

```text
50022 example.org 22
```

Ожидаемый вывод:

```text
Tunnel configured: local=50022, remote=example.org:22
```

## Запуск тестов

```bash
python3 -m unittest -v test_adapter.py
```
