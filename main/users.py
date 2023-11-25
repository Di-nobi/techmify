#!/usr/bin/env python3
"""Users Table"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from main.base import Main
from uuid import uuid4
Base = declarative_base()


class User(Base):
    """Users table setup"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    reset_token = Column(String(250), nullable=True)
    session_id = Column(String(100), nullable=True)
    # def __init__(self, *args: list, **kwargs: dict):
    #     """Initializes the instance"""
    #     self.id = kwargs.get('id', str(uuid4()))
