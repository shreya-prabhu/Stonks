import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

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
@app.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     next_url = request.form.get("next")

    #     if username in users and users[username][1] == password:
    #         session["username"] = username
    #         if next_url:
    #             return redirect(next_url)
    #         return redirect(url_for("dashboard"))
    return render_template("login.html")

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

if __name__ == "__main__":
    app.run(debug=True)
