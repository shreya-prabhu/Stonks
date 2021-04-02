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
def company_1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM CompanyDB')
        account = cursor.fetchall()

        return render_template("Company.html", account = account,len=len(account))
#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        if request.method == "POST":
            companyname = request.form['companyname']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * from CompanyDB WHERE CName = %s', [companyname])
            data = cursor.fetchall()
            if len(data) == 0 and companyname == 'all':
                cursor.execute("SELECT * from CompanyDB")
                data = cursor.fetchall()
            return render_template('search.html', data=data)
    return render_template('login.html')
# end point for inserting data dynamicaly in the database
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        CompanyName1 = request.form['CompanyName']
        SecurityNo1 = request.form['SecurityNo']
        Limited_Stock_Exchange1 = request.form['Limited_Stock_Exchange']
        Rate1 = request.form['Rate']
        No_of_shares1 = request.form['No_of_shares']
        cursor.execute('INSERT INTO CompanyDB VALUES ( %s, %s, %s, %s, %s)', (CompanyName1, SecurityNo1, Limited_Stock_Exchange1, Rate1, No_of_shares1, ))
        mysql.connection.commit()
        return redirect("http://localhost:5000/search", code=302)
    return render_template('insert.html')
if __name__ == "__main__":
    app.run(debug=True)
