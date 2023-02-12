from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

db = "recipe_share"
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.recipies = []

    @staticmethod
    def validate_registration(data):
        is_valid = True

        #first name validation
        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters", "first_name")
            is_valid = False

        #last name validation
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters", "last_name")
            is_valid = False

        #email validation
        #check for valid format
        if not email_regex.match(data["email"]):
            flash("Invalid email", "email")
            is_valid = False
        elif User.get_one_by_email({"email": data["email"]}):
            flash("Email already in use", "email")
            is_valid = False

        #password validation

        return is_valid

    @classmethod
    def get_one_by_email(cls, data):
        query = '''
            SELECT * 
            FROM users
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def insert(cls, data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(passord)s);
        '''
        return connectToMySQL(db).query_db(query, data)

    