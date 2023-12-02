#!/usr/bin/env python3
"""
Main file
"""
from main.auth import Auth
username = 'dinny'
firstname = 'Dracula'
lastname = 'King'
email = 'dracula100@yahoo.com'
password = '22'
auth = Auth()

auth.register_user(email, password, username, firstname, lastname)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

