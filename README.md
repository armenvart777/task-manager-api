# Task Manager API

A RESTful API for managing tasks built with Python and Flask. Supports full CRUD operations, filtering, priority levels, and task statistics.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks (supports `?status=` and `?priority=` filters) |
| GET | `/api/tasks/:id` | Get a single task |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/:id` | Update a task |
| DELETE | `/api/tasks/:id` | Delete a task |
| GET | `/api/stats` | Get task statistics |

## Quick Start

```bash
git clone https://github.com/armenvart777/task-manager-api.git
cd task-manager-api
pip install -r requirements.txt
python app.py
```

## Usage Examples

**Create a task:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Build a REST API", "priority": "high"}'
```

**Get all tasks:**
```bash
curl http://localhost:5000/api/tasks
```

**Filter by status:**
```bash
curl http://localhost:5000/api/tasks?status=pending
```

**Update a task:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Task Schema

```json
{
  "id": 1,
  "title": "Learn Flask",
  "description": "Build a REST API",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-02-25T12:00:00",
  "updated_at": "2026-02-25T12:00:00"
}
```

**Status values:** `pending`, `in_progress`, `completed`
**Priority values:** `low`, `medium`, `high`

## License

MIT
