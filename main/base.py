#!/usr/bin/env python3
"""Base File"""
import json
from datetime import datetime
# from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
import main
from sqlalchemy import Column, String

# Base = declarative_base()


class Main():
    """Base Model of the application"""
    id = Column(String(60), primary_key=True)
    def __init__(self, *args: list, **kwargs: dict):
        """Initializes the instance"""
        self.id = kwargs.get('id', str(uuid4()))

    def __eq__(self, other):
        """Checks for equality"""
        if type(self) != type(other):
            return False
        return (self.id == other.id)
    def to_json(self, serial: bool = False):
        """Converts the object to a json dictionary"""
        data = {}
        for k,v in self.__dict__.items():
            if not serial and k[0] == '_':
                continue
            else:
                data[k] = v
        return data
    def save(self):
        """Saves the data to the database"""
        main.store.new(self)
        main.store.save()