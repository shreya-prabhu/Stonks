import sqlite3
from flask import Flask, render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='root'
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
            session['username'] = request.form['username']
            session['username'] = account['username']
            session['T_ID'] = 0
            return render_template('admin_dashboard.html', msg = msg)

        cursor.execute('SELECT * FROM client_profile WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = request.form['username']
            return redirect("http://localhost:5000/dashboard", code=302)
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    if session['loggedin'] == False:
        return redirect("http://localhost:5000/login")
    return render_template('dashboard.html')

@app.route("/explorestocks")
def explorestocks():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT SCode, CName, Price FROM stocks;')
    stocklist = cursor.fetchall()
    return render_template('explorestocks.html', stocks = stocklist)

@app.route("/buy_stock")
def buy_stock():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT SCode, Price FROM stocks;')
    stocklist = cursor.fetchall()
    return render_template('buy.html', stocks=stocklist)

@app.route("/sell_stock")
def sell_stock():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    cursor = mysql.connection.cursor()
    username =session['username']
    cursor.execute('SELECT stock_customer.SCode, quantity, Price FROM stock_customer INNER JOIN stocks ON stock_customer.SCode = stocks.SCode where stock_customer.CName = %s;',[username])
    stocklist = cursor.fetchall()
    print(stocklist)
    return render_template('sell.html', stocks =stocklist)

@app.route("/trade")
def trade():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    return render_template('trade.html')

@app.route("/transactions")
def transactions():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    cursor = mysql.connection.cursor()
    username = session['username']
    cursor.execute(' SELECT S.CName from stocks S  left join transactions T on (T.Scode = S.Scode) where T.CName = %s;',[username])
    companieslist = cursor.fetchall()
    comp = []
    for c in companieslist:
        if c not in comp:
            comp.append(c)
    # companieslist = companieslist.values()
    # comp = set(comp)
    for company in comp:
        company_name = company["CName"]
        print("company",company_name)

        cursor.execute('SELECT T.T_ID,T.CName, T.T_Time,T.T_Date,T.T_type,S.SCode,T.Quantity,S.CName as Company_Name,S.SDescription,S.Price, round(T.Quantity*S.Price,2) as total \
            from stocks S  left join transactions T on (T.Scode = S.Scode) where T.CName=%s order by Company_Name',[username]);
        transactionlist = cursor.fetchall()
    return render_template('transactions.html', transactions = transactionlist, companies = comp)



@app.route("/profile")
def profile():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        username = session['username']
        print("i am ", username)
        cursor.execute('SELECT * FROM client_profile WHERE username = %s', [username])
        account = cursor.fetchone()
        return render_template("profile.html", account = account)
    
@app.route("/update_client", methods =['GET', 'POST'])
def update_client():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM client_profile WHERE username = %s', [username])
            account = cursor.fetchone()
            if account:
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address !'
                else:
                    cursor.execute('UPDATE client_profile SET  username =%s, password =%s, email_id =%s,phone_no =%s WHERE username =% s',(username,password,email,phonenumber,session['username']  ))
                    mysql.connection.commit()
                    msg = 'You have successfully updated !'
                    return redirect(url_for('dashboard'))
<<<<<<< HEAD
=======
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
>>>>>>> 68be3a6f9377437af2772d51281b9bffc0f4661b
        return render_template("update_client.html", msg = msg)
    return redirect(url_for('login'))

@app.route("/admin_profile")
def admin_profile():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin_profile WHERE username = %s', (session['username'], ))
        account = cursor.fetchone()
        return render_template("admin_profile.html", account = account)

@app.route("/Company")
def company_1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM CompanyDB')
        account = cursor.fetchall()

        return render_template("Company.html", account = account,len=len(account))

    return redirect('login')
#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        companyname = request.form['companyname']
        #companyname=string(companyname)
        # search by author or book
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * from CompanyDB WHERE CName = %s', [companyname])
        #cursor.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and companyname == 'all':
            cursor.execute("SELECT * from CompanyDB")

            data = cursor.fetchall()

        return render_template('search.html', data=data)
    return render_template('search.html')
# end point for inserting data dynamicaly in the database
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        CompanyName1 = request.form['CompanyName']
        SecurityNo1 = request.form['SecurityNo']
        Limited_Stock_Exchange1 = request.form['Limited_Stock_Exchange']

        No_of_shares1 = request.form['No_of_shares']
        cursor.execute('INSERT INTO CompanyDB VALUES (  %s, %s, %s, %s)', (CompanyName1, SecurityNo1, Limited_Stock_Exchange1, No_of_shares1, ))
        mysql.connection.commit()
        return redirect("http://localhost:5000/search", code=302)
    return render_template('insert.html')
@app.route("/Delete", methods=['GET', 'POST'])
def delete():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        CompanyName1 = request.form['CompanyName']
        cursor.execute('DELETE from CompanyDB WHERE CName = %s', [CompanyName1])
        mysql.connection.commit()
        return redirect("http://localhost:5000/Company", code=302)
    return render_template('Delete.html')

@app.route("/update", methods =['GET', 'POST'])
def update():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'oldCName' in request.form and 'CName' in request.form and 'SecurityNo' in request.form and 'Limited_Stock_Exchange' in request.form and 'No_of_shares' in request.form:
            CName1 = request.form['oldCName']
            CName2 = request.form['CName']
            SecurityNo1 = request.form['SecurityNo']
            Limited_Stock_Exchange1 = request.form['Limited_Stock_Exchange']

            No_of_shares1 = request.form['No_of_shares']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM CompanyDB WHERE CName = % s', (CName1, ))
            account = cursor.fetchone()
            cursor.execute('UPDATE companydb SET  CName =% s, SecurityNo =% s, Limited_Stock_Exchange =% s, No_of_shares =% s WHERE CName =% s',(CName2, SecurityNo1, Limited_Stock_Exchange1, No_of_shares1,CName1))
            mysql.connection.commit()
            msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg = msg)
    return render_template('update.html')

@app.route('/client_insert', methods=['GET', 'POST'])
def client_insert():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        username = request.form['username']
        password = request.form['password']
        aadharnumber = request.form['aadharnumber']
        pannumber = request.form['pannumber']
        securitycode = request.form['securitycode']
        dpid = request.form['dpid']
        bankacc = request.form['bankacc']
        bankname= request.form['bankname']
        bankifsc = request.form['bankifsc']
        banktype = request.form['banktype']
        cursor.execute('INSERT INTO client_profile VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (fullname, dob, email, phonenumber, username, password, aadharnumber, pannumber, securitycode, dpid , bankacc))
        mysql.connection.commit()
        cursor.execute('INSERT INTO bank_details VALUES ( %s ,%s, %s, %s )' ,( bankname, bankacc, bankifsc, banktype))
        mysql.connection.commit()
        return redirect("http://localhost:5000/login", code=302)
    return render_template('register.html')

@app.route('/buy_check', methods=['GET', 'POST'])
def buy_check():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        username = session['username']
        print(session['username'])
        num1 = request.form['num1']
        num1 =int(num1)
        stockid = request.form.get('name')
        stockid= str(stockid)
        cursor.execute('SELECT CName FROM stocks WHERE SCode = %s ', [stockid])
        query1 = cursor.fetchone()
        company= query1['CName']
        cursor.execute('SELECT No_of_shares FROM CompanyDB WHERE CName = %s ', [company])
        query2 = cursor.fetchone()
        number= int(query2['No_of_shares'])
        if num1<number:
            num2= number-num1
            cursor.execute('UPDATE CompanyDB SET No_of_shares = %s WHERE CName =%s;',(num2,company))
            mysql.connection.commit()
            query3=cursor.fetchone()
            if query3:
                num2 = int(query3['quantity'])
                cursor.execute('UPDATE stock_customer SET quantity = %s WHERE CName =%s AND SCode =%s;',(num1+num2,username,stockid))
            else:
                cursor.execute('Insert into stock_customer values(%s,%s,%s)',(stockid,username,num1))
            mysql.connection.commit()
            #cursor.execute('SELECT T_ID FROM transactions')
            #query4 = cursor.fetchall()
            #if query4:
            #    session['T_ID'] = int(query4[len(query4)-1]['T_ID'])+1
            #    T_ID =session['T_ID']
            #else:
            #    T_ID = session['T_ID'] =0
            #session['T_ID'] = session['T_ID']+1
            dateTimeObj = datetime.now()
            T_Time=str(dateTimeObj.hour)+':'+str(dateTimeObj.minute)+':'+str(dateTimeObj.second)+'.'+str(dateTimeObj.microsecond)
            T_Date= str(dateTimeObj.year)+'-'+str(dateTimeObj.month)+'-'+str(dateTimeObj.day)
            T_type ="Buy"
            cursor.execute('Insert into transactions values(%s,%s,%s,%s,%s,%s,%s)',(0,username, T_Time, T_Date, T_type, stockid, num1))
            mysql.connection.commit()
            return redirect("http://localhost:5000/transactions", code=302)
        return redirect("http://localhost:5000/dashboard", code=302)


@app.route('/sell_check', methods=['GET', 'POST'])
def sell_check():
    if 'loggedin' not in session:
        return redirect("http://localhost:5000/login")
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        username = session['username']
        num1 = request.form['num1']
        num1 =int(num1)
        stockid = request.form.get('name')
        stockid= str(stockid)
        cursor.execute('SELECT quantity FROM stock_customer WHERE SCode = %s ', [stockid])
        query1 = cursor.fetchone()
        if query1:
            quantity= int(query1['quantity'])
            if(num1-quantity>0):
                msg="Quantity is more than that bought"
                return render_template("/dashboard.html", code=302,msg=msg)
            cursor.execute('SELECT CName FROM stocks WHERE SCode = %s ', [stockid])
            query1 = cursor.fetchone()
            company= query1['CName']
            cursor.execute('SELECT No_of_shares FROM CompanyDB WHERE CName = %s ', [company])
            query2 = cursor.fetchone()
            number= int(query2['No_of_shares'])
            num2= number+num1
            cursor.execute('UPDATE CompanyDB SET No_of_shares = %s WHERE CName =%s;',(num2,company))
            mysql.connection.commit()
            if(quantity-num1 !=0):
                cursor.execute('UPDATE stock_customer SET quantity = %s WHERE CName =%s AND SCode =%s;',(quantity-num1,username,stockid))
            else:
                cursor.execute('DELETE from stock_customer where CName =%s AND SCode =%s;',(username,stockid))
            mysql.connection.commit()
            cursor.execute('SELECT T_ID FROM transactions')
            query4 = cursor.fetchall()
            """
            if query4:
                session['T_ID'] = int(query4[len(query4)-1]['T_ID'])+1
                T_ID =session['T_ID']
            else:
                T_ID = session['T_ID'] =0
            session['T_ID'] = session['T_ID']+1
            """
            dateTimeObj = datetime.now()
            T_Time=str(dateTimeObj.hour)+':'+str(dateTimeObj.minute)+':'+str(dateTimeObj.second)+'.'+str(dateTimeObj.microsecond)
            T_Date= str(dateTimeObj.year)+'-'+str(dateTimeObj.month)+'-'+str(dateTimeObj.day)
            T_type ="Sell"
            cursor.execute('Insert into transactions values(%s,%s,%s,%s,%s,%s,%s)',(0,username, T_Time, T_Date, T_type, stockid, num1))
            mysql.connection.commit()
            return redirect("http://localhost:5000/transactions", code=302)
        return redirect("http://localhost:5000/dashboard", code=302)

if __name__ == "__main__":
    app.run(debug=True)
