import json 
from flask import Flask, request, render_template
from pymongo import mongo_client 
from random import randint
from account import Account
from user import User

#need to finish adding new user
#connect users.json with mongoDB

app = Flask(__name__)

users = []
current_user = None #user that is currently logged in

def load_database(users):
    users_file = open("users.json")
    users_data = json.load(users_file)

    for u in users_data["users"]:
        accounts = []
        for acc in u["saved_accounts"]:
            accounts.append(Account(acc["name"],acc["username"], acc["password"]))

        users.append(User(u["username"], u["password"], accounts)) 
        

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
            current_user = i
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

def get_accounts(username):
    for i in users:
        if i.getName() == username:
            return i.getAccounts()

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
    return render_template("main_page.html", content = "Welcome "+username, accounts = get_accounts(username))


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

def write_account_json(new_account, username):
    with open('users.json') as json_file: 
        data = json.load(json_file) 
        for i in data['users']:
            if i['username'] == username:
                temp = i['saved_accounts']
                temp.append(new_account)
                write_json(data)

@app.route("/new_account/")
def new_account_page():
    return render_template("new_account_page.html")

@app.route("/new_account/<string:username>", methods = ["GET","POST"])
def add_new_account(username):
    if request.method == "POST":
        account = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        conf_pass = request.form.get("confirm_password")

        new_acc = {
            "name": account,
            "username": username,
            "password": password
        }
        write_account_json(new_acc, current_user.getName())

    return main_page(current_user.getName())




load_database(users)
app.run()
