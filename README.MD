# Tiser - API-сервис управления рекламными объявлениями (тизерами).
![CI](https://github.com/RuslanSibgatulin/Tiser_drf/actions/workflows/test.yml/badge.svg)

## [Постановка задачи](./task.md)

## Используемые технологии
- Код приложения на Python
- Фреймворк [Django 4.1](https://docs.djangoproject.com/en/4.1/) + [DRF](https://www.django-rest-framework.org/#installation)
- Swagger документация [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/index.html)
- СУБД - Postgres
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Клонировать репозиторий
    git@github.com:RuslanSibgatulin/Tiser_drf.git

## Переменные окружения
Подготовить файлы с переменными окружения по аналогии с файлами `docker/envs/*.example` и пересохранить в файлы `*.env`

## Запуск
    make start

### При первичном запуске необходимо выполнить команды инициализации
    make init

# Функционал
- [Админ-панель](http://127.0.0.1/admin/)
- [OpenAPI документация](http://127.0.0.1/apidocs/)
