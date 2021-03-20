import json 
import flask
from pymongo import mongo_client 
from random import randint
from account import Account
from user import User


#input() is gonna be textBox.Text from flask
#need to add gui
#connect users.json with mongoDB

users = []
current_user = User("","",[])
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

def login(users):
    print("Login\n")
    print("Username: ")
    username=input()  

    print("Password: ")
    password= input()

    for i in users:
        if i.getName() == username and i.getPassword() == password:
            current_user = i
            logged_in_menu(current_user)
        else:
            continue

    return False
  
def check_existing_username(username):
    with open('users.json') as f:
        data = json.load(f)
        for i in data['users']:
            if username == i['username']:
                return False
        return True

def register_new_user(users):
    print("Register\n")
    print("Username: ")
    username = input()

    while not check_existing_username(username):
        print("Username already exists. Try new: ")
        username = input()
        if check_existing_username(username):
            valid_username = username
            break

    print("Password: ")
    password = input()

    print("Confirm Password: ")
    ag_password = input()

    if password == ag_password:
        new_user = {
            "username": valid_username,
            "password": ag_password,
            "saved_accounts": []
        }
        users.append(User(new_user["username"], new_user["password"], new_user["saved_accounts"]))
    update_database(new_user)
    login(users)
        
def login_menu(users):
    print("1. Login\n2. Register")
    print("Input: ")
    x = int(input()) 

    if x == 1:
        login(users)

    elif x==2:
        register_new_user(users)
    

def logged_in_menu(user):
    print("Logged in")
    print("1.Display Accounts\n2.Add new account")
    print(type(current_user))

    x = int(input())

    if x==1:
        display_saved_accounts(user)
    elif x==2:
        add_new_saved_account(user)
       

def display_saved_accounts(user):
    print(user.print_savedAccounts())
    for i in user.getAccounts():
        print(i.getName())
    return
        
def write_account_json(new_account, username):
    with open('users.json') as json_file: 
        data = json.load(json_file) 
        for i in data['users']:
            if i['username'] == username:
                temp = i['saved_accounts']
                temp.append(new_account)
                write_json(data)

def add_new_saved_account(user):
    print("Profile: ")
    profile = input()
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()

    new_account = {
        "name": profile,
        "username": username,
        "password": password
    }
    write_account_json(new_account, user.getName())
    return


load_database(users)
login_menu(users)




