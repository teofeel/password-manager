import json as js
import django as dj
from pymongo import mongo_client 


class User:
    def __init__(self, name, password, saved_accounts):
        self.__name = name 
        self.__password = password
        self.__saved_accounts = saved_accounts

    def setName(self, name):
        self.__name = name

    def setPassword(self, password):
        self.__password = password

    def getPassword(self):
        return self.__password

    def getName(self):
        return self.__name 

    def comparePassword(self, password):
        if self.__password == password:
            return True
        else:
            return False

    def getAccounts(self):
        return self.__saved_accounts

    def print_savedAccounts(self):
        stringneki =  self.__name + "\n"

        for i in self.__saved_accounts:
            stringneki += i.printAccount() + "\n"

        return stringneki


    