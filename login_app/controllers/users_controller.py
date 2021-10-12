from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt 
from werkzeug import datastructures
from login_app import app
from login_app.models.user import User

bcrypt = Bcrypt(app)

#Index page
@app.route("/")
def index():
    return render_template("index.html")

#home page
@app.route("/home")
def home():
    if 'id' not in session:
        return redirect('/')
    return render_template("home.html")    

#Add a new user - register.
@app.route("/new_user", methods=["POST"])
def addUser():
    data = {
        "fName": request.form["fName"],
        "lName" : request.form["lName"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "doblepassword" : request.form["doblepassword"],
        "encrypted_password" : bcrypt.generate_password_hash(request.form['password'])
    }
    verify=User.user_at_db(data)
    if (len(verify)) < 1:
        if not User.validate_user(data):
            return redirect('/')
        User.add_user(data)
        flash("Thank you. Please login with your information.")
    else:
        flash("Email already registered")
    return redirect('/')

#Login
@app.route("/authentication", methods=['POST'])
def validation():
    email = request.form["email"]
    password = request.form["password"]
    verifyemail=User.validate_email(email)
    if verifyemail == ():
            flash("Email not registered")
            return redirect("/")
    else:
        password_at_db = verifyemail[0]['password']
        if verifyemail[0]['email'] == email:
            if bcrypt.check_password_hash(password_at_db, password):
                session.clear()
                data={
                    'id':verifyemail[0]['id'],
                    'fName': verifyemail[0]['fName']
                }
                session['id'] = verifyemail[0]['id']
                session['name'] = verifyemail[0]['fName']
                print (session['id'], session['name'])
                return redirect("/home")
            else:
                flash("Wrong password, try again")
    return redirect('/')
    
#Logout
@app.route("/logout", methods=['GET'])
def logout_session():
    session.clear()
    return redirect('/')