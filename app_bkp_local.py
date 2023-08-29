import flask
import sqlite3
import flask.url_for as url_for
import flask.request as request
import flask.redirect as redirect
import flask.render_template as render_template

app = flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.row
    return conn


@app.route('/travelblog/home')
def home():
    return render_template('index.html', msg='', login=url_for("login"))


# http://localhost:5000/travelblog/ - the following will be our login page, which will use both get and post requests
@app.route('/travelblog/login', methods=['get', 'post'])
def login():
    # output message if something goes wrong...
    if request.method == 'post' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_db = find_user_login(username)
        if password == password_db:
            return redirect(url_for("profile", username=username))
    return render_template('login.html', msg="")


@app.route('/travelblog/register', methods=['get', 'post'])
def register():
    # output message if something goes wrong...
    msg = ''
    # check if "username", "password" and "email" post requests exist (user submitted form)
    if request.method == 'post' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_db = find_user_login(username)
        if not password_db:
            insert_query_user(username=username, email=email, password=password)
        else:
            msg = 'user already exists! please try to login'
            return redirect(url_for("login"))
        return redirect(url_for("profile", username=username))
    elif request.method == 'post':
        msg = 'please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/travelblog/profile/<username>')
def profile(username):
    return render_template('profile.html', username1=username)


@app.route('/travelblog/logout')
def logout():
    return render_template('login.html', msg="")


if __name__ == "__main__":
    app.run(debug=True)
