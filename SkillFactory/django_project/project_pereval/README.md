
---

# REST API для создания базы горных перевалов

REST API для сервиса добавления, редактирования и просмотра перевалов, с возможностью загрузки фотографий и контроля модерации.

---

## Цель проекта

Разработать API для управления информацией о горных перевалах, которые пользователи (туристы) могут отправлять на сервер Федерации Спортивного Туризма России (ФСТР) с указанием координат, описаний, сложности маршрутов и сопутствующих изображений.

---

## Реализованные возможности

- `POST /submitData/` — добавление нового перевала
- `GET /submitData/<id>/` — просмотр конкретного перевала по ID
- `PATCH /submitData/<id>/edit/` — редактирование перевала (если статус `new`)
- `GET /submitData/user/?user__email=<email>` — получение списка перевалов пользователя
- Автоматическая документация через Swagger UI (drf-spectacular)

---

## Стек технологий

- Django / Django REST Framework
- PostgreSQL
- Swagger UI — визуальная документация OpenAPI
- Django Filter — фильтрация по email
- Pytest — тестирование API и бизнес-логики

---

## Как пользоваться API

### 1. Добавить перевал

**Endpoint:** `POST /submitData/`  
**Тело запроса:** JSON

```json
{
  "beautytitle": "Плато",
  "title": "Хребет Таганай",
  "other_titles": "Таганай",
  "connect": "соединяет два ущелья",
  "user": {
    "email": "hiker@example.com",
    "phone": "+79112223344",
    "last_name": "Иванов",
    "first_name": "Пётр",
    "patronymic": "Алексеевич"
  },
  "coords": {
    "latitude": 55.17133,
    "longitude": 59.66522,
    "height": 1345
  },
  "area": 1,
  "winter_level": "2A",
  "summer_level": "1B",
  "autumn_level": "1A",
  "spring_level": "1A"
}
```

Для загрузки изображений используйте `multipart/form-data` или Swagger-интерфейс.

---

### 2. Получить перевал по ID

**Endpoint:** `GET /submitData/<id>/`  
**Ответ:** JSON, включает вложенные объекты и поле `status`

---

### 3. Редактировать перевал

**Endpoint:** `PATCH /submitData/<id>/edit/`  
**Условия:** редактирование возможно только при `status = "new"`  
**Ответ:**
```json
{
  "state": 1,
  "message": "Запись успешно обновлена"
}
```

---

### 4. Получить список перевалов по email

**Endpoint:** `GET /submitData/user/?user__email=example@example.com`  
**Ответ:** массив объектов перевалов

---

## Документация API

Swagger-документация доступна по адресу:  
[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

Сгенерирована с помощью `drf-spectacular`, включает описание запросов, схемы вложенных объектов (`user`, `coords`, `images`), примеры и ошибки.

---

## Тестирование

В проекте реализовано покрытие бизнес-логики (`SubmitDataService`) и REST API через интеграционные и модульные тесты:

- Создание, редактирование и получение перевала
- Проверка отклонения PATCH при статусе ≠ `"new"`
- Фильтрация по email
- Проверка вложенных моделей (`user`, `coords`, `images`)

### Запуск тестов

```bash
pytest -v
```

Для проверки покрытия:

```bash
pytest --cov=pereval --cov-report=term-missing
```

### Структура тестов

```
tests/
├── test_integration_submit.py      # submit → PATCH → GET
├── test_filter_by_email.py         # фильтрация по email
├── conftest.py                     # фикстуры: api_client и др.
```

### Используемые инструменты

- `pytest`, `pytest-django`
- `APIClient` из `rest_framework.test`
- `SimpleUploadedFile` — для изображений
- Фикстура `api_client` в `conftest.py`

---

## Структура проекта

```
project_pereval/
├── manage.py
├── pereval/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   └── submit_data_service.py
├── tests/
│   ├── test_integration_submit.py
│   ├── test_filter_by_email.py
│   └── conftest.py
├── README.md
```

---

## Автор

Система разработана как учебно-практический проект - "Виртуальная стажировка" на платформе SkillFactory.

Студент курса PDEV-66 (PDEV-76)

Кузнецов Дмитрий

<dimon1734@yandex.ru>

---
