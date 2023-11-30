#!/usr/bin/env python3
from main.users import MongoDBUser
from main.chatRequest import ChatRequest
from colorama import Fore
from mongoengine import connect
from bson import ObjectId
from mongoengine import DoesNotExist

connect(alias='core', host='mongodb://localhost:27017/techmify')

classes = {"MongoDBUser": MongoDBUser}
class DBStorage:
    def add_user(self, email, hashed_password, username, firstname, lastname):
        user = MongoDBUser(email=email, hashed_password=hashed_password, username=username, firstname=firstname,
                           lastname=lastname)
        user.save()
        return user
    
    def get_user(self, **kwargs):
        user = MongoDBUser.objects(**kwargs).first()
        if not user:
            return None
        return user
    
    def update_user(self, user_id, **kwargs):
        DATA = ["id", "session_id", "email", "hashed_password", "reset_token"]
        try:
            user_id = ObjectId(user_id)
        except ValueError:
            raise ValueError("Invalid id")
        user = self.get_user(id=user_id)
        if user:
            for key, value in kwargs.items():
                if key not in DATA:
                    raise ValueError
                setattr(user, key, value)
            user.save()
            return None
        else:
            raise ValueError("User not found")
        
    def all(self, cls=None):
        """Gets a query of all the data in the database"""
        new_dict = {}
        if cls:
            data = self.__client.techmify[cls.__name__]
            obejs = data.find()
            for count in obejs:
                key = str(count['_id'])
                new_dict[key] = cls(**obejs)
        for i, j in classes.items():
            collec = self.__client.techmify[i]
            objes = collec.find()
            for count in objes:
                key = str(count['_id'])
                new_dict[key] = j(**objes)
        return new_dict
    
    def get(self, cls, id):
        """Gets a specific data"""
        try:
            usr_id = ObjectId(id)
        except ValueError:
            raise ValueError("Invalid id")
        
        try:
            usr = cls.objects(id=usr_id).first()
        except DoesNotExist:
            raise ValueError(f"{cls.__name__} does not exist")
        if type(usr) is ChatRequest:
            from_id = usr.from_id
            to_id = usr.to_id
            return { "from_id": from_id, "to_id": to_id }
        return usr