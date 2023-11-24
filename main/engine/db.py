#!/usr/bin/env python3
"""Database """

import main
from main.users import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from main.base import Main, Base
from sqlalchemy.orm.exc import NoResultFound 

classes = {"User": User}

class DBStorage:
    """Dialogues with MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiating the database"""
        TECH_USER = getenv('TECH_USER')
        TECH_PWD = getenv('TECH_PWD')
        TECH_HOST = getenv('TECH_HOST')
        TECH_DB = getenv('TECH_DB')
        TECH_ENV = getenv('TECH_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(TECH_USER,
                                             TECH_PWD,
                                             TECH_HOST,
                                             TECH_DB))
    
    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        session_fac = sessionmaker(bind=self.__engine)
        Session = scoped_session(session_fac)
        self.__session = Session
        
    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        """Saves data to the MySQL database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes data from the database"""
        self.__session.delete(obj)

    def add_user(self, username: str, firstname: str, lastname: str,
                 hashed_password: str, email: str):
        """Adds a user to the database
        Args:
            username
            email
            firstname
            lastname
            password
            """
        user = User(username=username, hashed_password=hashed_password, email=email,
                    firstname=firstname, lastname=lastname)
        self.new(user)
        self.save()
        return user

    def get_user(self, **kwargs):
        """Gets a user in the database"""
        user = self.__session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user"""
        DATA = ["id", "username", "firstname", "lastname", "hashed_password", "email"]
        user = self.get_user(id = user_id)
        for key, value in kwargs.items():
            if key not in DATA:
                raise ValueError
            setattr(user, key, value)
        self.save()
        return None
    
    def all(self, cls):
        """Gets all data on the database"""
        data = dict()
        for clas in classes:
            if not clas:
                obj = self.__session.query(clas).all()
                for count in obj:
                    get_key = count.__class__.__name__+ '.' + count.id
                    data[get_key] = count
        return data
    def get(self, cls, id):
        """Gets the object based on the class name and ID"""
        all_clas = main.store.all(cls)
        for val in all_clas.values():
            if (val.id == id):
                return val
        return None
    
    def close(self):
        """Calls the remove method"""
        self.__session.remove()