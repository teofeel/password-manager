import json 
import django as dj
from pymongo import mongo_client 
from random import randint
from account import Account
from user import User

#need to create main functionality
#need to add gui
#connect users.json with mongoDB

users_file = open("users.json")
users_data = json.load(users_file)

accounts = []
users = []


#from saved_accounts we retrieve data(name of website,username/email, password) and import it in users

for u in users_data["users"]:
    for acc in u["saved_accounts"]:
       accounts.append(Account(acc["name"],acc["username"], acc["password"]))

    users.append(User(u["username"], u["password"], accounts))  

for i in users:
    print (i.print_savedAccounts())

