const columns = [
  { status: "backlog", id: "backlog-list" },
  { status: "in_progress", id: "in-progress-list" },
  { status: "done", id: "done-list" },
];

const form = document.querySelector("#task-form");
const formMessage = document.querySelector("#form-message");
const boardMessage = document.querySelector("#board-message");

function addText(parent, tagName, className, value) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  element.textContent = value;
  parent.append(element);
  return element;
}

function createTaskCard(task) {
  const card = document.createElement("article");
  card.className = `task-card priority-${task.priority}`;
  addText(card, "h4", "task-title", task.title);
  if (task.description) addText(card, "p", "task-description", task.description);

  const metadata = document.createElement("div");
  metadata.className = "task-meta";
  addText(metadata, "span", "team-chip", task.team);
  addText(metadata, "time", "due-date", `до ${task.due_date}`);
  card.append(metadata);

  const controls = document.createElement("label");
  controls.className = "status-control";
  addText(controls, "span", "visually-hidden", "Статус задачи");
  const select = document.createElement("select");
  select.setAttribute("aria-label", `Статус задачи: ${task.title}`);
  for (const [value, label] of [["backlog", "Бэклог"], ["in_progress", "В работе"], ["done", "Готово"]]) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    option.selected = task.status === value;
    select.append(option);
  }
  select.addEventListener("change", async () => {
    await updateStatus(task.id, select.value);
  });
  controls.append(select);
  card.append(controls);
  return card;
}

async function loadTasks() {
  boardMessage.textContent = "";
  try {
    const response = await fetch("/api/tasks");
    if (!response.ok) throw new Error("Не удалось получить список задач");
    const tasks = await response.json();
    for (const column of columns) {
      const list = document.getElementById(column.id);
      const items = tasks.filter((task) => task.status === column.status);
      list.replaceChildren(...items.map(createTaskCard));
      list.closest(".board-column").querySelector(".count").textContent = String(items.length);
      if (items.length === 0) addText(list, "p", "empty-state", "Пока пусто");
    }
  } catch (error) {
    boardMessage.textContent = error.message;
  }
}

async function updateStatus(taskId, status) {
  try {
    const response = await fetch(`/api/tasks/${taskId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Не удалось изменить статус");
    await loadTasks();
  } catch (error) {
    boardMessage.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.textContent = "";
  const values = Object.fromEntries(new FormData(form).entries());
  try {
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Не удалось добавить задачу");
    form.reset();
    formMessage.textContent = "Задача добавлена";
    await loadTasks();
  } catch (error) {
    formMessage.textContent = error.message;
  }
});

loadTasks();
