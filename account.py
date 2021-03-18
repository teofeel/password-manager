import json as js
import django as dj
from pymongo import mongo_client 
from random import randint


class Account:
    def __init__(self,account_name, username, password):
        self.__account_name = account_name
        self.__username = username
        self.__password = password
        
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name

    def setPass(self, password):
        self.__password = password
    
    def getPass(self):
        return self.__password

    def setUsername(self, username):
        self.__username = username
    
    def getUsername(self):
        return self.__username

    def printAccount(self):
        return self.__account_name + " "+self.__username + " " + self.__password


