# Trust Ads

Это backend для сервиса объявлений написаный на Django REST Framework с аутентификацией пользователя, ролями, публикацией объявлений, отзывами и поиском.

## Особенности

- Регистрация и авторизация пользователей через JWT
- Разделение на роли: обычный пользователь и админ
- Смена пароля и сброс через email
- CRUD операции для объявлений
  - Пользователи могут управлять своими объявлениями
  - Админы могут управлять любыми объявлениями
- Отзывы на объявления с CRUD и разрешениями
- API документация Swagger и Redoc (через `drf-spectacular`)
- CORS настроены для интеграции frontend'а
- Проект обёрнут в docker для удобного запуска через `docker compose`

## Стек проекта

- Python 3.13+
- Django 5.x
- Django REST Framework
- PostgreSQL
- Simple JWT для аутентификации
- drf-spectacular для документации
- Docker & Docker Compose
- Nginx
- Pytest

## Настройка

### Зависимости

- Docker и Docker Compose установлены

### Запуск локально через Docker

1. Склонируйте репозиторий:
```bash
git clone https://github.com/github-main-user/trust-ads.git
cd trust-ads
```

2. Настройте переменные окружения:
```shell
cp .env.example .env
```

3. Соберите и запустите контейнеры:
```bash
docker compose up --build
```

4. Backend API будет доступен на: `http://localhost:80/`

- `http://localhost:80/api/v1/docs/` - документация swagger
- `http://localhost:80/api/v1/redoc/` - документация redoc
- `http://localhost:80/admin/` - админ панель

### Админ панель
Для создания администратора используйте эту команду:
```shell
docker compose exec web python manage.py createsuperuser
```

С целью демонстрации некоторые данные были предварительно заготовлены в фикстуры.
Загрузить их можно этой командой:
```shell
docker compose exec web python manage.py loaddata fixtures.json
```

## Тесты

Команда для запуска тестов:
```shell
docker compose run --rm web pytest
```

### Покрытие тестами

Чтобы увидеть покрытие запустите команду ниже:
```shell
docker compose run --rm web bash -c "coverage run -m pytest && coverage report"
```

## Notes

* Администратор имеет полный контроль над объявлениями и отзывами.
* Анонимные пользователи могут только просматривать список объявлений
* Объявления и отзывы сортированы по дате создания *(в низходящем порядке)*
* Пагинация ограничевает вывод до 4х оъявлений на страницу.
* Процесс сброса пароля основан на email, используя токен.

