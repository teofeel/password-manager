import json 
import flask
from pymongo import mongo_client 
from random import randint
from account import Account
from user import User


#dont know how to add new user to json file
#input() is gonna be textBox.Text from flask
#need to add gui
#connect users.json with mongoDB

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
    with open(filename,'w+') as f: 
        json.dump(data, f, ensure_ascii=False) 

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
            logged_in_menu(i)
        else:
            continue

    return False
  

def register_new_user(users):
    print("Register\n")
    print("Username: ")
    username = input()

    print("Password: ")
    password = input()

    print("Confirm Password: ")
    ag_password = input()

    if password == ag_password:
        new_user = {
            "username": username,
            "password": ag_password,
            "saved_accounts": None
        }
        users.append(User(new_user["username"], new_user["password"], new_user["saved_accounts"]))
    login(users)
    update_database(new_user)
        
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
    print("1. Display Accounts\n2.Add new account")

    x = int(input())

    if x==1:
        display_saved_accounts(user)
    elif x==2:
        add_new_saved_account(user)
       

def display_saved_accounts(user):
    print(user.print_savedAccounts())
        

#def add_new_saved_account(user):


load_database(users)
login_menu(users)




