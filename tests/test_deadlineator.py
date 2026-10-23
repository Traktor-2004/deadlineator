import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deadlineator import (  # noqa: E402
    add_task,
    calculate_priority,
    change_status,
    list_tasks,
    make_task,
    read_tasks,
)


class TaskValidationTests(unittest.TestCase):
    def test_make_task_trims_text_and_sets_default_status(self):
        task = make_task("  Подготовить показ  ", "2027-02-10", team="QA")
        self.assertEqual(task["title"], "Подготовить показ")
        self.assertEqual(task["status"], "backlog")
        self.assertEqual(task["team"], "QA")

    def test_title_is_required(self):
        with self.assertRaisesRegex(ValueError, "title is required"):
            make_task("  ", "2027-02-10")

    def test_due_date_must_be_a_real_iso_date(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            make_task("Проверить сборку", "2027-02-30")
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            make_task("Проверить сборку", "2027-W06-2")

    def test_priority_and_team_must_be_known_values(self):
        with self.assertRaisesRegex(ValueError, "priority"):
            make_task("Задача", "2027-02-10", priority="urgent")
        with self.assertRaisesRegex(ValueError, "team"):
            make_task("Задача", "2027-02-10", team="Marketing")

    def test_priority_score_uses_impact_and_urgency_over_effort(self):
        self.assertEqual(calculate_priority(4, 5, 2), 10.0)

    def test_priority_score_rejects_values_outside_scale(self):
        with self.assertRaisesRegex(ValueError, "from 1 to 5"):
            calculate_priority(6, 3, 2)


class TaskStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = Path(self.temp_dir.name) / "data" / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_storage_is_an_empty_list(self):
        self.assertEqual(read_tasks(self.storage), [])

    def test_add_task_persists_and_lists_by_date_then_priority(self):
        add_task(self.storage, title="Позже", due_date="2027-03-01", priority="high")
        add_task(self.storage, title="Скоро обычная", due_date="2027-02-01")
        add_task(self.storage, title="Скоро срочная", due_date="2027-02-01", priority="high")
        self.assertEqual(
            [task["title"] for task in list_tasks(self.storage)],
            ["Скоро срочная", "Скоро обычная", "Позже"],
        )

    def test_change_status_updates_the_saved_task(self):
        task = add_task(self.storage, title="Демо", due_date="2027-03-01")
        changed = change_status(self.storage, task["id"], "in_progress")
        self.assertEqual(changed["status"], "in_progress")
        self.assertEqual(read_tasks(self.storage)[0]["status"], "in_progress")

    def test_change_status_rejects_unknown_task_and_status(self):
        with self.assertRaises(KeyError):
            change_status(self.storage, "0000000000", "done")
        with self.assertRaisesRegex(ValueError, "status must be"):
            change_status(self.storage, "0000000000", "paused")


if __name__ == "__main__":
    unittest.main()
