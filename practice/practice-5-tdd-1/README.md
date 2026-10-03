# Практика 5 (TDD-1): Числа Fibonacci на Python

В этой директории находится Python-реализация практики №5.
В методичке используется C# и MSTest, а здесь та же структура и TDD-последовательность
переведены на Python и `unittest`.

## Файлы

- `fibonacci.py`: класс `Fibonacci` и статический метод `fibonacci(n)`.
- `test_fibonacci.py`: тесты, повторяющие шаги из методички.
- `main.py`: консольная точка входа для разового расчета.

## Запуск приложения

Из текущей директории:

```bash
python3 main.py
```

После запуска введите число, например `10`, и нажмите Enter.

Ожидаемый вывод:

```text
55
```

## Запуск тестов

```bash
python3 -m unittest -v test_fibonacci.py
```

## Генерация PyDoc

```bash
python3 -m pydoc fibonacci
python3 -m pydoc main
python3 -m pydoc test_fibonacci
```

## Перевод сниппетов C# -> Python

### Шаг 1: Начальный метод и первый тест

C# (из методички):

```csharp
public static int Fibonacci(int n)
{
    return 0;
}

[TestMethod]
public void TestFirstFibonacciNumber()
{
    Assert.AreEqual(0, Fibonacci.Fibonacci(0));
}
```

Python (в этом проекте):

```python
@staticmethod
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    ...

def test_first_fibonacci_number(self) -> None:
    self.assertEqual(0, Fibonacci.fibonacci(0))
```

### Шаг 2: Добавление второго теста

C# (из методички):

```csharp
[TestMethod]
public void TestSecondFibonacciNumber()
{
    Assert.AreEqual(1, Fibonacci.Fibonacci(1));
}
```

Python (в этом проекте):

```python
def test_second_fibonacci_number(self) -> None:
    self.assertEqual(1, Fibonacci.fibonacci(1))
```

### Шаг 3: Добавление третьего и четвертого тестов

C# (из методички):

```csharp
[TestMethod]
public void TestThirdFibonacciNumber()
{
    Assert.AreEqual(1, Fibonacci.Fibonacci(2));
}

[TestMethod]
public void TestForthFibonacciNumber()
{
    Assert.AreEqual(2, Fibonacci.Fibonacci(3));
}
```

Python (в этом проекте):

```python
def test_third_fibonacci_number(self) -> None:
    self.assertEqual(1, Fibonacci.fibonacci(2))

def test_fourth_fibonacci_number(self) -> None:
    self.assertEqual(2, Fibonacci.fibonacci(3))
```

### Шаг 4: Финальная реализация Fibonacci

C# (из методички):

```csharp
public static int Fibonacci(int n)
{
    if (n == 0)
        return 0;
    else if (n == 1)
        return 1;
    else return Fibonacci(n - 1) + Fibonacci(n - 2);
}
```

Python (в этом проекте):

```python
@staticmethod
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return Fibonacci.fibonacci(n - 1) + Fibonacci.fibonacci(n - 2)
```
