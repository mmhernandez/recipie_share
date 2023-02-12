from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import user

@app.route("/")
def login_registration():
    return render_template("/login_registration.html")

@app.route("/register", methods=["POST"])
def register():
    if user.User.validate_registration(request.form):
        session["id"] = user.User.insert(request.form)
        return redirect("/all_recipies")
    else:
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    return redirect("/all_recipies")



@app.route("/clear_form")
def clear_form():
    session.clear()
    return redirect("/")
