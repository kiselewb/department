# API организационной структуры

REST API для управления иерархической структурой подразделений и сотрудников.

## Стек

- **FastAPI** + **SQLAlchemy 2.0** (async) + **PostgreSQL**
- **Alembic** - миграции
- **Pydantic v2** - валидация данных
- **loguru** - логирование
- **pytest** + **pytest-asyncio** - тесты
- **uv** - управление зависимостями
- **Docker** + **docker-compose**

## Структура проекта

```
app/
├── api/v1/endpoints/   # Роутеры (departments, employees)
├── config/             # Настройки, пути, логирование
├── database/           # Сессия БД
├── models/             # SQLAlchemy модели
├── repositories/       # Слой работы с БД
├── schemas/            # Pydantic схемы
├── services/           # Бизнес-логика
└── utils/              # Исключения
alembic/                # Миграции
tests/                  # Интеграционные тесты
```

## Запуск через Docker

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd <repo-dir>
```

### 2. Создать `.env` из примера

```bash
cp .env.example .env
```

> В `.env` убедитесь, что `DB_HOST=db` (для Docker-сети).

### 3. Запустить

```bash
docker-compose up -d -build
```

Приложение запустится на [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs).  
Миграции применяются автоматически перед стартом.

---

## Локальный запуск (без Docker)

### Требования

- Python 3.13+
- PostgreSQL (запущенный локально)
- uv

### 1. Установить зависимости

```bash
uv sync
```

### 2. Настроить `.env`

```bash
cp .env.example .env
# Изменить DB_HOST=localhost
```

### 3. Применить миграции

```bash
uv run alembic upgrade head
```

### 4. Запустить сервер

```bash
uv run fastapi run app/main.py
```

---

## Тесты

Для тестов нужна отдельная БД (задаётся через `TEST_DB_NAME` в `.env`).

```bash
uv run pytest
```

---

## API

Документация доступна после запуска:

- **Swagger UI**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

### Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/departments/` | Список всех подразделений |
| `POST` | `/api/v1/departments/` | Создать подразделение |
| `GET` | `/api/v1/departments/{id}` | Дерево подразделения (`depth`, `include_employees`) |
| `PATCH` | `/api/v1/departments/{id}` | Обновить подразделение |
| `DELETE` | `/api/v1/departments/{id}` | Удалить (`mode=cascade\|reassign`) |
| `POST` | `/api/v1/departments/{id}/employees/` | Добавить сотрудника |
| `GET` | `/api/v1/employees/` | Список всех сотрудников |

### Особенности бизнес-логики

- Имена подразделений уникальны в рамках одного родителя
- Подразделение не может быть родителем самому себе
- При перемещении подразделения выполняется проверка на цикл (рекурсивный CTE)
- Удаление в режиме `reassign` переносит сотрудников в указанное подразделение
- Удаление в режиме `cascade` удаляет всё дерево вместе с сотрудниками