from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
#email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# special_chars = ['$','&','!','%']

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post


class User:
    def __init__(self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    #class method to save user to the database
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name, email, password)VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        #data is a dictionary that will be passed into the save method from server.py
        #this return statement would return an integer of the id we just created in the database
        return connectToMySQL("dojo_wall").query_db(query,data)
    
    
    # #This is a static method to validate a new user (register)
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("dojo_wall").query_db(query,user)
        if len(results) >= 1:
            flash("Email Already Taken By Another User","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email Invalid","register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First Name must consist of at least 3 characters","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must consist of at least 3 characters","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must consist of at least 8 characters","register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password entered doesn't match","register")
        return is_valid


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        return cls(results[0])


