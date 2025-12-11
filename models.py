from app import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(10), nullable=False, default="user")
    # "user" or "admin"

    tasks = db.relationship("Task", backref="owner", lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    status = db.Column(db.String(20), nullable=False, default="pending")
    # pending / done

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20), nullable=False)  # "created" / "deleted"
    task_title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", backref="task_logs")

