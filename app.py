from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'paper_prototype_secret_key'

INITIAL_TASKS = [
    {
        "id": 1,
        "title": "画面設計書の作成",
        "category": "設計",
        "assignee": "山田",
        "priority": "高",
        "status": "進行中",
        "due_date": "2026-10-10"
    },
    {
        "id": 2,
        "title": "要件定義ヒアリング",
        "category": "企画",
        "assignee": "鈴木",
        "priority": "中",
        "status": "完了",
        "due_date": "2026-10-01"
    }
]

tasks_db = list(INITIAL_TASKS)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "管理者")
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    total_tasks = len(tasks_db)
    in_progress = sum(1 for t in tasks_db if t["status"] == "進行中")
    not_started = sum(1 for t in tasks_db if t["status"] == "未着手")
    completed = sum(1 for t in tasks_db if t["status"] == "完了")

    return render_template(
        "dashboard.html",
        total_tasks=total_tasks,
        in_progress=in_progress,
        not_started=not_started,
        completed=completed
    )

@app.route("/tasks")
def task_list():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("tasks/index.html", tasks=tasks_db)

@app.route("/tasks/add", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("login"))

    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": new_id,
        "title": request.form.get("title", "新規タスク"),
        "category": request.form.get("category", "開発"),
        "assignee": request.form.get("assignee", session.get("user", "担当者")),
        "priority": request.form.get("priority", "中"),
        "status": request.form.get("status", "未着手"),
        "due_date": request.form.get("due_date", "2026-10-30")
    }
    tasks_db.append(new_task)
    return redirect(url_for("task_list"))

@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user" not in session:
        return redirect(url_for("login"))

    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return redirect(url_for("task_list"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)