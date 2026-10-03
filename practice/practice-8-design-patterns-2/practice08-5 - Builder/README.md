# Практика 8-5: Builder (Python)

Реализован паттерн `Builder` для генерации электронной книги в двух форматах: `HTML` и `FB2`.

## Что реализовано

- `builders.py`: абстракция `BookBuilder` и реализации `HTMLBookBuilder`, `FB2BookBuilder`.
- `composer.py`: абстрактный директор `BookComposer`.
- `generate_romeo_and_juliet.py`: прикладной генератор и конкретный директор `RomeoAndJulietComposer`.
- `main.py`: CLI-запуск и парсинг аргументов, делегирование в `generate_romeo_and_juliet.py`.
- `test_builder.py`: unit-тесты (логика построения, запись файлов, запуск CLI).

## Диаграмма классов

```text
+------------------+                +------------------------+
|   BookComposer   | <------------- | RomeoAndJulietComposer |
+------------------+    inherits    +------------------------+
        |
        | uses
        v
+------------------+                +------------------------+
|   BookBuilder    | <------------- |    HTMLBookBuilder     |
+------------------+    inherits    +------------------------+
        ^
        | inherits
        |
+------------------------+
|     FB2BookBuilder     |
+------------------------+
```

## Запуск приложения

Сгенерировать HTML-книгу:

```bash
python3 main.py html output.html
```

Сгенерировать FB2-книгу:

```bash
python3 main.py fb2 output.fb2
```

Пример вывода в консоль:

```text
Файл успешно создан: output.html
```

## Запуск тестов

```bash
python3 -m unittest -v test_builder.py
```
