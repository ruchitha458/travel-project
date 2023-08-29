import sqlite3

def find_user_login(username):
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    sql_query = 'SELECT distinct password FROM users where username = "' + username + '";'
    t = cur.execute(sql_query).fetchall()
    return str("".join(t[0]))
    
def select_all_users():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    all_users = cur.execute("select * from users").fetchall()
    return [user for user in all_users]

def create_table():
   connection = sqlite3.connect('database.db') 
   with open('schema.sql') as f:
        connection.executescript(f.read())
    
def insert_query_user(username, email, password):
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password))
    connection.commit()
    connection.close()
    return "Record Inserted Successfully"
