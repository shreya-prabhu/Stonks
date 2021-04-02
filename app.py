import sqlite3
from flask import Flask, render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='password'
app.config['MYSQL_DB'] = 'stonks'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    return render_template('register.html')

# Route for handling the login page logic
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin_profile WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            msg = 'Logged in successfully !'
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['username']
            return render_template('admin_dashboard.html', msg = msg)
        cursor.execute('SELECT * FROM client_profile WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
    return render_template('login.html')
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin_profile WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            msg = 'Logged in successfully !'
            return render_template('admin_dashboard.html', msg = msg)

    return render_template('login.html')

    #return render_template('login.html', error=error)

old login page
@app.route("/login1")
def login1():
    return render_template('login1.html')
'''
@app.route("/logout")
def logout():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/explorestocks")
def explorestocks():
    return render_template('explorestocks.html')

@app.route("/trade")
def trade():
    return render_template('trade.html')

@app.route("/transactions")
def transactions():
    return render_template('transactions.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')
@app.route("/admin_profile")
def admin_profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin_profile WHERE username = % s', (session['username'], ))
        account = cursor.fetchone()
        return render_template("admin_profile.html", account = account)
if __name__ == "__main__":
    app.run(debug=True)
