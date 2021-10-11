from flask import render_template, request, redirect, session, flash
from login_app import app
from login_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def getStart():
    return render_template("index.html")

@app.route("/add_user", methods=['POST'])
def add_new_user():
    fName = request.form['firstname']
    lName = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    encrypted_password = bcrypt.generate_password_hash(password)
    doble_password = request.form['doblepassword']


    if User.validate_data(fName, lName, email, encrypted_password, password, doble_password):
        nuser = User(fName, lName, email, encrypted_password)
        User.addUser(nuser)
        return redirect("/")
    else:
        print("something went wrong")
        return redirect("/")

#Para Login
#@app.route("/login", methods=['POST'])
#def displayLogin():
#    loginError = ""
#    if 'loginError' in session:
#        loginError = session['loginError']
#    return render_template("index.html", loginError=loginError)


@app.route('/authentication', methods=['POST'])                           
def validateCredentials():
    email = request.form ['email']
    password = request.form ['password']
    result = User.validate_Email(email)
    if result == ():
        flash("Email not registered")
        return redirect("/")
    else:
        verificated_password = result[0]['password']
        if result[0]['email'] == email:
            if bcrypt.check_password_hash(verificated_password, password):
                session.clear()
                data={
                    'id':result[0]['id'],
                    'fName': result[0]['fName']
                    }
                session['id'] = result[0]['id']
                print(session['id'])
                return redirect("/home")
            else:
                flash("Wrong credentials provided.")
    return redirect ('/')

@app.route("/home", methods=['GET'])
def get_home():
    if 'id' not in session:
        return redirect('/')
    user_info = User.start_session(session['id'])
    data = {
        "id": session['id'],
        "fName": user_info[0]['fName']
    }
    return render_template("home.html", info=data)

@app.route("/logout", methods=['GET'])
def logout_session():
    session.clear()
    return redirect("/")