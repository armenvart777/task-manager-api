# Task Manager API — Менеджер задач

RESTful API для управления задачами на Python и Flask. Полный CRUD, фильтрация, приоритеты и статистика.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite)

## API Эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/tasks` | Получить все задачи (фильтры: `?status=`, `?priority=`) |
| GET | `/api/tasks/:id` | Получить одну задачу |
| POST | `/api/tasks` | Создать новую задачу |
| PUT | `/api/tasks/:id` | Обновить задачу |
| DELETE | `/api/tasks/:id` | Удалить задачу |
| GET | `/api/stats` | Статистика по задачам |

## Быстрый старт

```bash
git clone https://github.com/armenvart777/task-manager-api.git
cd task-manager-api
pip install -r requirements.txt
python app.py
```

## Примеры использования

**Создать задачу:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Изучить Flask", "description": "Создать REST API", "priority": "high"}'
```

**Получить все задачи:**
```bash
curl http://localhost:5000/api/tasks
```

**Фильтр по статусу:**
```bash
curl http://localhost:5000/api/tasks?status=pending
```

**Обновить задачу:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Схема задачи

```json
{
  "id": 1,
  "title": "Изучить Flask",
  "description": "Создать REST API",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-02-25T12:00:00",
  "updated_at": "2026-02-25T12:00:00"
}
```

**Статусы:** `pending`, `in_progress`, `completed`
**Приоритеты:** `low`, `medium`, `high`

## Лицензия

MIT
