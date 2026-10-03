# Практика 7-3: Abstract Factory (Python)

Реализован паттерн `Abstract Factory` для создания семейств врагов в зависимости
от уровня сложности игры.

## Что реализовано

- `difficulty_level.py`:
  - перечисление `DifficultyLevel` (`easy`, `hard`).
- `enemies.py`:
  - базовый класс `Enemy` и его наследники;
  - конкретные враги для easy- и hard-уровней;
  - имя врага задается через конструктор.
- `enemy_factory.py`:
  - абстрактная фабрика `AbstractEnemyFactory`;
  - конкретные фабрики `EasyLevelEnemyFactory`, `HardLevelEnemyFactory`;
  - обобщенный метод `create(...)` и обобщенная функция `make_named_enemy(...)`.
- `main.py`: консольная демонстрация создания врага.
- `test_enemy_factory.py`: unit-тесты.

## Диаграмма классов

```text
+---------------------------+   inherits   +----------------------+
|   EasyLevelEnemyFactory   | -----------> |                      |
+---------------------------+              |                      |
                                           | AbstractEnemyFactory |
+---------------------------+   inherits   |                      |
|   HardLevelEnemyFactory   | -----------> |                      |
+---------------------------+              +----------------------+
                                                    |
                                                    | creates markers
                                                    v
                                              +-------------+
                                              |   Soldier   |
                                              +-------------+
                                              +-------------+
                                              |   Monster   |
                                              +-------------+
                                              +-------------+
                                              | SuperMonster|
                                              +-------------+
```

## Запуск приложения

```bash
python3 main.py
```

Введите одну строку формата:

`difficulty enemy_type name`

Где:
- `difficulty`: `easy` или `hard`
- `enemy_type`: `soldier`, `monster`, `supermonster`

Пример:

```text
hard monster Kraken
```

Пример вывода:

```text
BadMonster(name=Kraken, power=70, difficulty=hard)
```

## Запуск тестов

```bash
python3 -m unittest -v test_enemy_factory.py
```
