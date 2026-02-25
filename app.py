import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, g, jsonify, request

app = Flask(__name__)
DATABASE = "tasks.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    db.commit()


def require_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks with optional filtering."""
    db = get_db()
    status = request.args.get("status")
    priority = request.args.get("priority")

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)

    query += " ORDER BY created_at DESC"
    tasks = db.execute(query, params).fetchall()

    return jsonify({
        "tasks": [dict(task) for task in tasks],
        "count": len(tasks)
    })


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a single task by ID."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(task))


@app.route("/api/tasks", methods=["POST"])
@require_json
def create_task():
    """Create a new task."""
    data = request.get_json()

    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    valid_priorities = ("low", "medium", "high")
    priority = data.get("priority", "medium")
    if priority not in valid_priorities:
        return jsonify({"error": f"Priority must be one of: {valid_priorities}"}), 400

    now = datetime.now().isoformat()
    db = get_db()
    cursor = db.execute(
        "INSERT INTO tasks (title, description, priority, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (data["title"], data.get("description", ""), priority, now, now),
    )
    db.commit()

    task = db.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(task)), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@require_json
def update_task(task_id):
    """Update an existing task."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    valid_statuses = ("pending", "in_progress", "completed")
    valid_priorities = ("low", "medium", "high")

    status = data.get("status", task["status"])
    priority = data.get("priority", task["priority"])

    if status not in valid_statuses:
        return jsonify({"error": f"Status must be one of: {valid_statuses}"}), 400
    if priority not in valid_priorities:
        return jsonify({"error": f"Priority must be one of: {valid_priorities}"}), 400

    now = datetime.now().isoformat()
    db.execute(
        "UPDATE tasks SET title=?, description=?, status=?, priority=?, updated_at=? WHERE id=?",
        (
            data.get("title", task["title"]),
            data.get("description", task["description"]),
            status,
            priority,
            now,
            task_id,
        ),
    )
    db.commit()

    updated = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return jsonify(dict(updated))


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()

    return jsonify({"message": f"Task {task_id} deleted successfully"})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get task statistics."""
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    pending = db.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
    in_progress = db.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    completed = db.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0]

    return jsonify({
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
    })


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
