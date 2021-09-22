from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.models import Doctor
from admin.forms import LoginForm


auth_blueprint = Blueprint("auth", __name__, url_prefix="/admin")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Doctor.authenticate(form.email.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("admin.index"))
        flash("Wrong user ID or password.", "danger")
    return render_template("login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("auth.login"))
