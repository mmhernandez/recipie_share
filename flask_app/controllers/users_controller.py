from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import user

@app.route("/")
def login_registration():
    return render_template("/login_registration.html")

@app.route("/register", methods=["POST"])
def register():
    registration_info = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if user.User.validate_registration(registration_info):
        session.clear()
        session["id"] = user.User.insert(registration_info)
        return redirect("/recipes")
    else:
        session["first_name"] = registration_info["first_name"]
        session["last_name"] = registration_info["last_name"]
        session["email"] = registration_info["email"]
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    if user.User.validate_login(request.form):
        logged_in_user = user.User.get_one_by_email({"email": request.form["email"]})
        session["id"] = logged_in_user.id
        return redirect("/recipes")
    return redirect("/")

@app.route("/logout")
def clear_form():
    session.clear()
    return redirect("/")
