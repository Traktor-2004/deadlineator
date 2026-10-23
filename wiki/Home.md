# Дедлайнатор

> Планер команды, который не даст дедлайнам исчезнуть в переписке.

## Содержание

- [О проекте](#о-проекте)
- [Навигация по вики](#навигация-по-вики)
- [Поток задачи](#поток-задачи)
- [Быстрый запуск](#быстрый-запуск)

## О проекте

«Дедлайнатор» помогает небольшой учебной команде вести задачи от бэклога до готового результата. Приложение работает локально, а GitFlic используется для исходного кода, вики, карточек задач и CI/CD.

## Навигация по вики

- [Описание продукта](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=Product.md)
- [Начало работы](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=Getting-started.md)
- [Архитектура](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=Architecture.md)
- [Правила команды](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=Team-work.md)
- [Локальная сборка и CI/CD](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=CI-CD.md)
- [Термины](https://gitflic.ru/project/dedlainator/dedlainator/wiki/page?file=Glossary.md)

## Поток задачи

| Этап | Что происходит | Следующий шаг |
| --- | --- | --- |
| Бэклог | Команда уточняет результат и критерии готовности | В работе |
| В работе | Разработка и локальная проверка | Проверка |
| Проверка | QA сверяет результат с критериями | Готово или возврат в работу |
| Готово | Результат принят и показан | Новая задача |

**Поток:** Бэклог → В работе → Проверка → Готово. Если проверка находит замечания, задача возвращается в работу.

## Быстрый запуск

В каталоге проекта выполните:

```powershell
py -3 scripts/seed_demo_data.py
py -3 src/server.py
```

Приложение откроется по адресу http://127.0.0.1:8000. Стартовый набор из десяти задач хранится в `data/demo_tasks.json`, а изменения пользователя — в локальном `data/tasks.json`, который не публикуется в Git.

## Материалы проекта

- [Доска из десяти учебных задач](https://gitflic.ru/project/dedlainator/dedlainator/issue?status=)
- [Квартальный план и диаграмма Ганта](https://gitflic.ru/project/dedlainator/dedlainator/blob?file=Block-3-Roadmap.md&branch=main)
- [Исходный код проекта](https://gitflic.ru/project/dedlainator/dedlainator/file?branch=main)

