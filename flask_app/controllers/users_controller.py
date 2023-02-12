from flask_app import app
from flask import render_template, session, redirect

@app.route("/")
def login_registration():
    return render_template("/login_registration.html")

@app.route("/clear_form")
def clear_form():
    session.clear()
    return redirect("/")
