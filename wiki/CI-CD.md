# Локальная сборка и CI/CD

GitFlic хранит исходный код и запускает pipeline. Runner выполняет команды локально на компьютере разработчика через Git Bash. Демонстрационное приложение доступно по адресу <http://127.0.0.1:8000>.

## Поток сборки

Коммит в GitFlic → локальный Windows Runner → компиляция Python-исходников → 10 модульных тестов → локальный релиз в deploy/releases.

## Pipeline

Конфигурация хранится в корне репозитория в файле gitflic-ci.yaml.

| Этап | Команда | Результат |
| --- | --- | --- |
| build | bash ./ci-verify.sh build | Проверка версии Python и компиляция исходников |
| test | bash ./ci-verify.sh test | Запуск 10 модульных тестов |
| deploy | bash ./ci-deploy.sh | Подготовка копии приложения и демо-данных в `deploy/releases` |

Каждая задача требует тег `local-windows`. GitFlic Runner версии 5.0.0 использует Shell executor с Git Bash. Проверочные скрипты используют Python 3.12 из профиля Windows. Стадия deploy сохраняет отдельную копию релиза на этом компьютере; публикация в Azure App Service не настроена.

## Проверенный запуск

Pipeline [№20](https://gitflic.ru/project/dedlainator/dedlainator/ci-cd/pipeline/20) для коммита `37ccf2b` завершился успешно на локальном агенте The Lord of the Eagles. Сборка, тесты и подготовка локального релиза прошли без ошибок. Журнал стадии test содержит результат `Ran 10 tests` и `OK`. Релиз размещён в каталоге `deploy/releases`.

## Настройка runner

Для Runner версии 5.0.0 требуются Java 17 и Git for Windows. Регистрационный токен создаётся в GitFlic; не сохраняйте его в файлах, логах, репозитории или истории команд.

Пример регистрации с подстановочными значениями:

~~~powershell
java -jar runner.jar register --url <URL_ИЗ_GITFLIC> --registration-token <ВРЕМЕННЫЙ_ТОКЕН>
~~~

Файл config/application.properties:

~~~properties
runner.executor=shell
runner.cli.shell=C:/Program Files/Git/bin/bash.exe
runner.cli.args=-c
logging.file.name=data/log/server.log
~~~

Запуск runner:

~~~powershell
java -jar runner.jar start --config=config/application.properties
~~~

## Локальный показ

Запустить приложение из каталога проекта:

~~~powershell
py -3 src/server.py
~~~

Затем открыть <http://127.0.0.1:8000>. Демо-набор из 10 задач создаётся командой `py -3 scripts/seed_demo_data.py`. Модульные тесты запускаются командой `py -3 -m unittest discover -s tests -v`.
