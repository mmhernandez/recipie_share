from flask_app import app
from flask import render_template

@app.route("/")
def login_registration():
    return render_template("/login_registration.html")