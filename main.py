#!/usr/bin/env python3
"""
Main file
"""

from main.engine.db import DBStorage
from main.users import User

my_db = DBStorage()

user_1 = my_db.add_user("Dwayne", "Dinobi", "Udeh", "Dinobi2002", "udehdinobi@gmail.com")
print(user_1.id)

# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id)