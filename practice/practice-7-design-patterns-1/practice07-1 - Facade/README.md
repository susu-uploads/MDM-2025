# Практика 7-1: Facade (Python)

## Что реализовано

- Класс `Estate` для передачи данных в фасад.
- Отдельные подсистемы расчета:
  - `ApartmentContributionCalculator`
  - `HouseWithLandContributionCalculator`
- Класс-фасад `CalculationFacade`, который:
  - скрывает детали выбора алгоритма;
  - делегирует расчет соответствующей подсистеме;
  - позволяет заменить алгоритм через `register_calculator`.

## Структура

- `calculation_facade.py` — доменная модель и фасад.
- `main.py` — консольный запуск.
- `test_calculation_facade.py` — unit-тесты.

## Диаграмма классов

```text
+-------------------------+   uses data   +------------------+   typed by   +------------------+
|    CalculationFacade    | ----------->  |      Estate      | -----------> |    EstateType    |
+-------------------------+               +------------------+              +------------------+
          |                                        |
          | delegates calculation                  | typed by
          v                                        v
+------------------------------+                  +------------------+
|   ContributionCalculator     |                  |    ValueGroup    |
+------------------------------+                  +------------------+
          ^            ^
          |            +----------------------+
          | inherits                          | inherits
+---------------------------------+   +-------------------------------------+
| ApartmentContributionCalculator |   | HouseWithLandContributionCalculator |
+---------------------------------+   +-------------------------------------+
```

## Запуск приложения

```bash
python3 main.py
```

Ожидается одна строка в формате:

`estate_type area_m2 cadastral_value residents_count value_group`

Где:

- `estate_type`: `apartment` или `house_with_land`
- `value_group`: `economy`, `comfort`, `premium`

Пример:

```text
apartment 60 5000000 3 comfort
```

Пример результата:

```text
599.04
```

## Запуск тестов

```bash
python3 -m unittest -v test_calculation_facade.py
```
