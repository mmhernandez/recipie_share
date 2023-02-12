from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import recipe, user

@app.route("/recipes")
def display_recipies():
    if "id" in session:
        recipe_list = recipe.Recipe.get_all_with_creator()
        user_info = user.User.get_one_by_id({"id": session["id"]})
        return render_template("all_recipes.html", recipes=recipe_list, user=user_info)
    return redirect("/")

@app.route("/recipe/new")
def new_recipe():
    if "id" in session:
        return render_template("add_recipe.html")
    return redirect("/")

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
            return redirect("/recipes")
        else:
            session["name"] = recipe_info["name"]
            session["description"] = recipe_info["description"]
            session["instructions"] = recipe_info["instructions"]
            session["date_cooked"] = recipe_info["date_cooked"]
            session["cooked_under_30m"] = recipe_info["cooked_under_30m"]
            return redirect("/new_recipe")
    return redirect("/")

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "id" in session:
        recipe_obj = recipe.Recipe.get_one_by_id({"id": id})
        return render_template("edit_recipe.html", recipe=recipe_obj)
    return redirect("/")

@app.route("/update_recipe/<int:id>", methods=["POST"])
def update_recipe(id):
    if "id" in session:
        recipe_info = {
            "id": id,
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_cooked": request.form["date_cooked"],
            "cooked_under_30m": request.form["under_30m"],
            "user_id": session["id"]
        }
        if recipe.Recipe.validate_recipe(recipe_info):
            recipe.Recipe.update_recipe(recipe_info)
            return redirect("/recipes")
        else:
            return redirect(f"/recipes/edit/{recipe_info['id']}")
    return redirect("/")