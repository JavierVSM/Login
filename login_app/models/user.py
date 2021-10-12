from werkzeug import datastructures
from login_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data):
        self.id = data['id']
        self.email = data['email']
        self.fName = data['fName']
        self.lName = data['lName']
        self.password = data['password']


    #New user  
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users ( fName , lName , email , password ) VALUES ( %(fName)s , %(lName)s , %(email)s , %(encrypted_password)s );"
        return connectToMySQL('login_db').query_db( query, data )

    @classmethod
    def user_at_db(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        return connectToMySQL('login_db').query_db( query, data)
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['fName']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(data['lName']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False 
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False    
        if data['password'] != data['doblepassword']:
            flash("Password confirmation does not match the first password, please try again")
            isValid = False
        return is_valid
    
    #Login:
    @classmethod
    def validate_email(cls, email):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        email={
            "email": email
        }
        result = connectToMySQL("login_db").query_db(query,email)
        return result
