# Начало работы

## Требования

- Windows, Linux или macOS;
- Python 3.10+;
- Git для работы с репозиторием.

Внешние Python-библиотеки не нужны.

## Запуск на Windows

```powershell
py -3 --version
py -3 scripts/seed_demo_data.py
py -3 src/server.py
```

Первая команда подготовки заполнит пустое хранилище десятью учебными задачами и не затронет уже существующие данные. Откройте <http://127.0.0.1:8000>. Сервер слушает только loopback-интерфейс компьютера.

## Запуск тестов

```powershell
py -3 -m unittest discover -s tests -v
```

## Остановка и данные

- Остановить сервер: `Ctrl+C` в окне терминала.
- Файл задач: `data/tasks.json`.
- Чтобы использовать другой файл, задайте переменную `DEADLINEATOR_DATA` перед запуском.

```powershell
$env:DEADLINEATOR_DATA = "$PWD\data\demo.json"
py -3 src/server.py
```
