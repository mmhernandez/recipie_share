from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "recipe_share"

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.cooktime_under_30m = data["cooktime_under_30m"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.creator = None

    @staticmethod
    def validate_recipe(data):
        print("Validating...")
        is_valid = True

        #name validation
        if len(data["name"]) < 1:
            flash("Name required", "name")
            is_valid = False
        elif len(data["name"]) < 3:
            flash("Name must be at least 3 characters", "name")
            is_valid = False

        #description validation
        if len(data["description"]) < 1:
            flash("Description required", "description")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("Description must be at least 3 characters", "description")
            is_valid = False

        #instructions validation
        if len(data["instructions"]) < 1:
            flash("Instructions required", "instructions")
            is_valid = False
        elif len(data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters", "instructions")
            is_valid = False

        #date cooked validation
        if len(data["date_cooked"]) < 1:
            flash("Date required", "date_cooked")
            is_valid = False

        #cook time validation
        if len(data["cooked_under_30m"]) < 1:
            flash("Cook time required", "under_30m")
            is_valid = False

        print(f"is_valid = {is_valid}")
        return is_valid
        
    @classmethod
    def get_all_with_creator(cls):
        query = '''
            SELECT * 
            FROM recipes R
            LEFT JOIN users U on U.id = R.user_id
            ORDER BY R.name;
        '''
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            recipe_obj = cls(row)
            user_info = {
                "id": row["U.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["U.created_at"],
                "updated_at": row["U.updated_at"]
            }
            recipe_obj.creator = user.User(user_info)
            recipes.append(recipe_obj)
        return recipes
    
    @classmethod
    def get_one_by_id(cls, data):
        query = '''
            SELECT * 
            FROM recipes
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def insert_recipe(cls, data):
        query = '''
            INSERT INTO recipes (name, description, instructions, date_cooked, cooktime_under_30m, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(cooked_under_30m)s, %(user_id)s);
        '''
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def update_recipe(cls, data):
        query = '''
            UPDATE recipes
            SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s,
                date_cooked = %(date_cooked)s,
                cooktime_under_30m = %(cooked_under_30m)s,
                user_id = %(user_id)s
            WHERE id = %(id)s;
        '''
        connectToMySQL(db).query_db(query, data)