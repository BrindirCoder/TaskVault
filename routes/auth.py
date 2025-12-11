from flask import Flask, request, redirect, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import (
    LoginManager,
    logout_user,
    login_required,
    login_user,
    current_user,
)
from models import User
from app import db


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            # USERNAME check
            if User.query.filter_by(username=username).first():
                return render_template("register.html", error="Username already taken.")

            # EMAIL check
            if User.query.filter_by(email=email).first():
                return render_template(
                    "register.html", error="Email already registered."
                )

            # PASSWORD length check
            if len(password) < 8:
                return render_template(
                    "register.html", error="Password must be at least 8 characters."
                )

            # PASSWORD strength check
            strong_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
            if not re.match(strong_regex, password):
                return render_template(
                    "register.html",
                    error="Weak password: use uppercase, lowercase, and numbers.",
                )

            # CONFIRMATION check
            if password != confirm_password:
                return render_template("register.html", error="Passwords do not match.")

            # Create user
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username, email=email, password_hash=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("dashboard"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password_hash, password):
                return render_template(
                    "login.html", error="Invalid username or password"
                )

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin_panel"))
            else:
                return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template(
            "dashboard.html", user=current_user, username=current_user.username
        )

    @app.route("/admin")
    @login_required
    def admin_panel():
        if current_user.role != "admin":
            return "Access Denied", 403  # or redirect to dashboard

        users = User.query.all()
        return render_template("admin_panel.html", users=users)

    @app.route("/admin/add_admin", methods=["GET", "POST"])
    @login_required
    def add_admin():
        if current_user.role != "admin":
            return "Access Denied", 403
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            hashed_password = generate_password_hash(password)

            new_admin = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                role="admin",
            )
            db.session.add(new_admin)
            db.session.commit()
            return redirect(url_for("admin_panel"))

        return redirect(url_for("admin_panel"))

    @app.route("/admin/delete_admin/<int:user_id>", methods=["POST"])
    @login_required
    def delete_admin(user_id):
        # Only admins can delete other admins
        if current_user.role != "admin":
            return "Access Denied", 403

        # Prevent deleting yourself
        if current_user.id == user_id:
            return "You cannot delete yourself.", 403

        admin = User.query.get_or_404(user_id)

        if admin.role != "admin":
            return "This user is not an admin.", 400

        # Optional: delete all tasks and logs of the admin
        for task in admin.tasks:
            db.session.delete(task)
        for log in admin.task_logs:
            db.session.delete(log)

        db.session.delete(admin)
        db.session.commit()

        return redirect(url_for("admin_panel"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))
