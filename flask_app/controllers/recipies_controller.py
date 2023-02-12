from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import recipe, user

@app.route("/all_recipes")
def display_recipies():
    if "id" in session:
        recipe_list = recipe.Recipe.get_all_with_creator()
        user_info = user.User.get_one_by_id({"id": session["id"]})
        return render_template("all_recipes.html", recipes=recipe_list, user=user_info)
    return redirect("/")

@app.route("/new_recipe")
def new_recipe():
    return render_template("add_recipe.html")

@app.route("/add_recipe", methods=["POST"])
def insert_recipe():
    if "id" in session:
        recipe_info = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_cooked": request.form["date_cooked"],
            "cooked_under_30m": request.form["under_30m"],
            "user_id": session["id"]
        }
        if recipe.Recipe.validate_recipe(recipe_info):
            recipe.Recipe.insert_recipe(recipe_info)
            if "name" in session:
                session.pop("name")
            if "description" in session:
                session.pop("description")
            if "instructions" in session:
                session.pop("instructions")
            if "date_cooked" in session:
                session.pop("date_cooked")
            if "cooked_under_30m" in session:
                session.pop("cooked_under_30m")
            return redirect("/all_recipes")
        else:
            session["name"] = recipe_info["name"]
            session["description"] = recipe_info["description"]
            session["instructions"] = recipe_info["instructions"]
            session["date_cooked"] = recipe_info["date_cooked"]
            session["cooked_under_30m"] = recipe_info["cooked_under_30m"]
            return redirect("/new_recipe")
    return redirect("/")
