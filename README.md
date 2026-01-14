# 🚗 Сервис автомобильных фар — FastAPI приложение

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

Веб-приложение для управления заявками на услуги по обслуживанию автомобильных фар  
с удобным веб-интерфейсом и REST API, реализованное на **FastAPI**.

---

## 📋 Функционал

- ✅ Просмотр всех заявок
- ✅ Добавление новой заявки
- ✅ Удаление заявки
- ✅ Перенос заявки на другую дату
- ✅ Фильтрация заявок по дате
- ✅ Веб-интерфейс на Jinja2
- ✅ Работа с датами (валидация, ограничения)

---

## 🛠 Технологии

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Jinja2, HTML, CSS, JavaScript
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic
- **Containerization**: Docker, Docker Compose

---

## 📁 Структура проекта

```text
PurrfectHeadlight/
├── app/
│   ├── __init__.py
│   ├── main.py              # Основное приложение FastAPI
│   ├── database.py          # Подключение и настройка БД
│   └── models.py            # SQLAlchemy модели
├── templates/
│   └── index.html           # HTML шаблон
├── requirements.txt         # Зависимости Python
├── docker-compose.yml       # Docker Compose конфигурация
├── Dockerfile               # Docker образ приложения
└── README.md                # Документация проекта
