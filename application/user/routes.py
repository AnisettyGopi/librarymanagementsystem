import time
from run import app
from flask import (
    Blueprint,
    jsonify,
    request,
    flash,
    redirect,
    render_template,
    url_for

)
from application import db
from application.user.models import User
from application.user.forms import UserRegistrationForm, UpdateUserForm
from application.error_handling import *


# creating blueprint
users = Blueprint("users", __name__, template_folder="templates")


# Home page routes
# @users.route("/")
@users.route("/home")
def home():
    return render_template("home.html", title="Home")


# Get all users and Post a new user
@users.route("/user", methods=["GET", "POST"])
def user_route():
    users = User.query.all()
    form = UserRegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created. Welcome " + new_user.username, "success")
        return redirect(url_for("users.user_route"))
    return render_template("user.html", users=users, form=form)


# Get user by username
@users.route("/user/<string:user_name>", methods=["GET"])
def get_user(user_name):
    # Get the required user from the user table
    required_user = User.query.filter_by(username=user_name).first()
    if required_user:
        flash("User found", "success")
    else:
        flash("No user exits", "warning")
        return redirect(url_for("users.user_route"))
    return render_template(
        "user_by_name.html", required_user=required_user, title="User"
    )


# Update user by user name
@users.route("/user/update/<string:user_name>", methods=["POST", "GET"])
def update_user(user_name):
    user_to_update = User.query.filter_by(username=user_name).first()
    if user_to_update:
        form = UpdateUserForm()
        if form.validate_on_submit():
            # Update the user with new details
            user_to_update.username = form.username.data
            user_to_update.email = form.email.data
            user_to_update.password = form.password.data
            db.session.commit()
            flash("User updated successfully", "success")
            return redirect(url_for("users.user_route"))
        elif request.method == "GET":
            form.username.data = user_to_update.username
            form.email.data = user_to_update.email

        return render_template("update_user.html", form=form, title="Update User")

    else:
        flash("Invalid username", "danger")


# Delete user by user_name
@users.route("/user/delete/<string:user_name>", methods=["POST", "GET"])
def delete_user(user_name):
    # Get the deleted user from user table
    user_to_delete = User.query.filter_by(username=user_name).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted successfully", "success")
        return redirect(url_for("users.user_route"))
    else:
        flash("Invalid username", "danger")
