#!/usr/bin/env python3
"""
Main file
"""
from main.auth import Auth

email = 'dinobi10022.com'
password = '22'
auth = Auth()

auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

