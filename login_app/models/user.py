from flask import flash, session
from login_app.config.mysqlconnection import connectToMySQL
import re

class User:
    def __init__( self , email, fName, lName, password):
        self.email = email
        self.fName = fName
        self.lName = lName
        self.password = password

    @classmethod
    def addUser(cls, nuser):
        query = "INSERT INTO users(email, fName, lName, password) VALUES (%(email)s, %(fName)s , %(lName)s , %(password)s);"
        data={
            "email": nuser.email,
            "fName": nuser.fName,
            "lName": nuser.lName,
            "password": nuser.password
        }
        result = connectToMySQL("login_db").query_db(query,data)
        return result
    
    @staticmethod
    def validate_data(fName, lName, email, encrypted_password, password, doble_password):
        isValid = True
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        query = "SELECT email FROM users WHERE email = %(email)s;"
        email_data = {
                "email" : email,
            }
        results = connectToMySQL("login_db").query_db(query,email_data)

        print(len(results))

        if not EMAIL_REGEX.match(email):
            flash("Invalid email, please write email in valid format")
            isValid = False

        elif results != False and results != ():
            flash("Email already registered")
            isValid = False

        if len( fName ) < 2:
            flash( "First name must be at least 2 characters long" )
            isValid = False 

        if len( lName ) < 2:
            flash( "Last name must be at least 2 characters long")
            isValid = False

        if len(password) < 8:
            flash("Password must be at least 8 characters long")
            isValid = False

        if password != doble_password:
            flash("Passwords must match, try again")
            isValid = False
        return isValid

     #Para login:
    @classmethod
    def get_user_to_validate(cls, email, password):
        query = "SELECT * FROM users WHERE email=%(email)s AND password=%(password)s;"
        data= {
            "email":email,
            "password":password
        }
        result = connectToMySQL('login_db').query_db(query, data)
        return result

    @classmethod
    def validate_Email(cls, email):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        email={
            "email": email
            }
        result = connectToMySQL("login_db").query_db(query,email)
        return result

    @classmethod
    def start_session(cls,data):
        query = "SELECT fName FROM users WHERE id = %(id)s;"
        data = {
            "id": session['id'],
        }
        results = connectToMySQL("login_db").query_db(query,data)
        return results
