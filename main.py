from flask import Flask, url_for, render_template, request, redirect, flash, session
from init_db import insert_query_user, create_table, find_user_login, select_all_users
from flask_session import Session
import os

app = Flask(__name__)

SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)


@app.route('/')
def home():
    return redirect(url_for("site_home"))

@app.route('/travelblog/home')
def site_home():
    return render_template('index.html', msg='', login=url_for("login"))

@app.route('/login')
def site_login():
    return redirect(url_for("login"))

# http://localhost:5000/travelblog/ - the following will be our login page, which will use both get and post requests
@app.route('/travelblog/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_db = find_user_login(username)
        if password_db.strip() != password.strip():
            error = 'Invalid User Credentials!'
            redirect(url_for("register"))
        else:
            return redirect(url_for("profile", username=username))
    return render_template('login.html', msg=error)


@app.route('/travelblog/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            password_db = find_user_login(username)
        except Exception:
            password_db = None
            insert_query_user(username=username, email=email, password=password)
        if not password_db:
            return redirect(url_for("profile", username=username))
        else:
            error = 'user already exists! please try to login'
            return redirect(url_for("login", msg=error))
    elif request.method == 'post':
        error = 'please fill out the form!'
    return render_template('register.html', msg=error)


@app.route('/travelblog/profile/<username>')
def profile(username):
    return render_template('profile.html', username1=username)


@app.route('/travelblog/logout')
def logout():
    return render_template('login.html', msg="")


if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
    app.run(debug=True)
