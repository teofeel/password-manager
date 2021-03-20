import json 
from flask import Flask, request, render_template
from pymongo import mongo_client 
from random import randint
from account import Account
from user import User

#need to add gui
#connect users.json with mongoDB

app = Flask(__name__)

users = []


def load_database(users):
    users_file = open("users.json")
    users_data = json.load(users_file)
    accounts = []
    #from saved_accounts we retrieve data(name of website,username/email, password) and import it in users
    for u in users_data["users"]:
        for acc in u["saved_accounts"]:
            accounts.append(Account(acc["name"],acc["username"], acc["password"]))

        users.append(User(u["username"], u["password"], accounts)) 
        account = []

def write_json(data, filename='users.json'):
    with open(filename,'w') as f: 
        json.dump(data,f)

def update_database(user):
    with open('users.json') as json_file: 
        data = json.load(json_file) 
        temp = data['users'] 
        temp.append(user)
        write_json(data)

def login(username, password):
    for i in users:
        if i.getName() == username and i.getPassword() == password:
            return True
        else:
            continue
    return False

def check_existing_username(username):
    for i in users:
        if username == i.getName():
            return False
    return True

def check_registry(username, password, conf_pass):
    if password != conf_pass:
        return 1
    elif not check_existing_username(username):
        return 2
    else:
        new_user = {
            "username": username,
            "password": password,
            "saved_accounts": []
        }
        update_database(new_user)
        return 3

@app.route('/')
def welcome_page():
    return render_template("welcome_page.html")

@app.route('/login/')
def login_page():
    return render_template("login_page.html")

@app.route('/login/', methods=["GET","POST"])
def login_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if login(username, password):
            return main_page(username)
        
    return render_template("login_page.html", content = "Username or password not matching. Try again")



@app.route('/')
def main_page(username):
    return render_template("main_page.html", content = username)


@app.route('/register/')
def register_page():
    return render_template("register_page.html")

@app.route('/register/', methods=["GET","POST"])
def register_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conf_pass = request.form.get("confirm_password")

        if check_registry(username, password, conf_pass) == 3:
            return main_page(username)

        elif check_registry(username, password, conf_pass) == 2:
            return render_template("register_page.html", content="Username already exists")

        elif check_registry(username, password, conf_pass) == 1:
            return render_template("register_page.html", content="Passwords don't match")

    return render_template("register_page.html", content="Uknown error")

@app.route("/add_account/")
def add_account_page():
    return render_template("new_account_page.html")

@app.route("/add_account/")
def add_new_account():
    return True

load_database(users)
app.run()
