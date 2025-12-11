from flask import Flask, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from models import Task, TaskLog
from app import db


def register_tasks(app):
    @app.route("/tasks")
    @login_required
    def task():
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template("task.html", tasks=tasks)

    @app.route("/add_task", methods=["GET", "POST"])
    @login_required
    def add_task():
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            status = request.form.get("status")

            new_task = Task(
                title=title,
                description=description,
                status=status,
                user_id=current_user.id,
            )
            db.session.add(new_task)
            db.session.commit()

        log = TaskLog(action="created", task_title=title, user_id=current_user.id)
        db.session.add(log)
        db.session.commit()

        return redirect(url_for("task"))

    @app.route("/delete/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_task(id):
        task = Task.query.get_or_404(id)
        log = TaskLog(action="deleted", task_title=task.title, user_id=task.user_id)
        db.session.add(log)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("task"))
