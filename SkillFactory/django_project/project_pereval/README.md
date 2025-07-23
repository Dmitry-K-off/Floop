
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


Конечно, Дмитрий — оформим раздел `Deployment` так, чтобы он был полезен не только тебе, но и всей команде, кто будет разворачивать проект. Вот шаблон, который можно вставить в `README.md`:

---

## Deployment (Yandex Cloud)

### Requirements

- Ubuntu VM в Яндекс Cloud с доступом по SSH  
- Установлены: `Python 3.12+`, `virtualenv`, `PostgreSQL`, `Nginx`, `gunicorn`
- Статический внешний IP (например, `89.169.190.82`)
- Зарезервированный PostgreSQL-пользователь с правами `CREATEDB`

---

### Шаги

```bash
# 1. Клонируем репозиторий
git clone https://github.com/<your-org>/project_pereval.git
cd project_pereval

# 2. Создаём виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Создаём и настраиваем файл .env
cp .env.template .env
nano .env  # Вставить параметры подключения к PostgreSQL

# 5. Миграции и статические файлы
python manage.py migrate
python manage.py collectstatic
```

---

### Gunicorn

Файл `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn daemon for Django project_pereval
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project_pereval/<project_path>
ExecStart=/home/ubuntu/project_pereval/venv/bin/gunicorn \
          project_pereval.wsgi:application \
          --bind 127.0.0.1:8000 --workers 3

Restart=always
EnvironmentFile=/home/ubuntu/project_pereval/<project_path>/.env

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

### Nginx

Файл `/etc/nginx/sites-available/project_pereval`:

```nginx
server {
    listen 80;
    server_name 89.169.190.82;

    location = / {
        return 302 /api/docs/;  # Редирект на Swagger
    }

    location /static/ {
        root /home/ubuntu/project_pereval/<project_path>;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Активировать и перезапустить:

```bash
sudo ln -s /etc/nginx/sites-available/project_pereval /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---


## Автор

Система разработана как учебно-практический проект - "Виртуальная стажировка" на платформе SkillFactory.

Студент курса PDEV-66 (PDEV-76)

Кузнецов Дмитрий

<dimon1734@yandex.ru>

---
