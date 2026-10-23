"""Core rules and local JSON storage for the Deadlineator project."""

from __future__ import annotations

import json
import os
import re
import tempfile
import uuid
from datetime import date
from pathlib import Path
from typing import Any


STATUSES = {"backlog", "in_progress", "done"}
PRIORITIES = {"low", "medium", "high"}
TEAMS = {"Core", "Web", "QA"}


def _required_text(value: Any, field: str, max_length: int) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    if len(text) > max_length:
        raise ValueError(f"{field} must be at most {max_length} characters")
    return text


def make_task(
    title: Any,
    due_date: Any,
    priority: Any = "medium",
    team: Any = "Core",
    description: Any = "",
) -> dict[str, Any]:
    """Validate user input and return a new task in the project's data format."""
    clean_title = _required_text(title, "title", 120)
    clean_date = _required_text(due_date, "due_date", 10)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", clean_date):
        raise ValueError("due_date must use YYYY-MM-DD format")
    try:
        date.fromisoformat(clean_date)
    except ValueError as exc:
        raise ValueError("due_date must use YYYY-MM-DD format") from exc

    clean_priority = str(priority or "medium").strip().lower()
    if clean_priority not in PRIORITIES:
        raise ValueError("priority must be low, medium, or high")

    clean_team = str(team or "Core").strip()
    if clean_team not in TEAMS:
        raise ValueError("team must be Core, Web, or QA")

    clean_description = str(description or "").strip()
    if len(clean_description) > 1000:
        raise ValueError("description must be at most 1000 characters")

    return {
        "id": uuid.uuid4().hex[:10],
        "title": clean_title,
        "description": clean_description,
        "due_date": clean_date,
        "priority": clean_priority,
        "team": clean_team,
        "status": "backlog",
    }


def calculate_priority(impact: int, urgency: int, effort: int) -> float:
    """Return a simple prioritization score on 1-5 input scales."""
    for name, value in (("impact", impact), ("urgency", urgency), ("effort", effort)):
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError(f"{name} must be an integer from 1 to 5")
    return round((impact * urgency) / effort, 2)


def read_tasks(path: str | Path) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError("task storage must contain a JSON list of objects")
    return data


def write_tasks(path: str | Path, tasks: list[dict[str, Any]]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(tasks, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix="tasks-", suffix=".json", dir=file_path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(encoded)
        os.replace(temporary_name, file_path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def add_task(path: str | Path, **values: Any) -> dict[str, Any]:
    task = make_task(**values)
    tasks = read_tasks(path)
    tasks.append(task)
    write_tasks(path, tasks)
    return task


def change_status(path: str | Path, task_id: str, status: str) -> dict[str, Any]:
    if status not in STATUSES:
        raise ValueError("status must be backlog, in_progress, or done")
    tasks = read_tasks(path)
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = status
            write_tasks(path, tasks)
            return task
    raise KeyError(task_id)


def list_tasks(path: str | Path) -> list[dict[str, Any]]:
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(
        read_tasks(path),
        key=lambda task: (
            task.get("due_date", "9999-12-31"),
            priority_order.get(task.get("priority"), 3),
            task.get("title", "").casefold(),
        ),
    )
