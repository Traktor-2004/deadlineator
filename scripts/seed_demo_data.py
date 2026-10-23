"""Create the sample task database for a fresh Deadlineator checkout."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILE = ROOT / "data" / "demo_tasks.json"
DATA_FILE = ROOT / "data" / "tasks.json"


def main() -> int:
    if DATA_FILE.exists():
        print("Локальные задачи уже существуют; файл оставлен без изменений.")
        return 0

    tasks = json.loads(SAMPLE_FILE.read_text(encoding="utf-8"))
    if not isinstance(tasks, list) or len(tasks) != 10:
        raise ValueError("В demo_tasks.json должны быть ровно 10 задач.")

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Создано локальное демо-хранилище: 10 задач.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
