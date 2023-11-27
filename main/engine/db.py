#!/usr/bin/env python3
from main.users import MongoDBUser
from colorama import Fore
from mongoengine import connect

connect(alias='core', host='mongodb://localhost:27017/techmify')
class DBStorage:
    def add_user(self, email, hashed_password):
        user = MongoDBUser(email=email, hashed_password=hashed_password)
        user.save()
        return user
    
    def get_user(self, **kwargs):
        user = MongoDBUser.objects(**kwargs).first()
        if not user:
            return None
        return user
    
    def update_user(self, user_id, **kwargs):
        DATA = ["id", "session_id", "email", "hashed_password", "reset_token"]
        user = self.get_user(id=user_id)
        for key, value in kwargs.items():
            if key not in DATA:
                raise ValueError
            setattr(user, key, value)
        user.save()
        return None
    