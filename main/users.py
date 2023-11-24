#!/usr/bin/env python3
"""Users Table"""
from sqlalchemy import Column, Integer, String
from main.base import Main, Base


class User(Main, Base):
    """Users table setup"""
    __tablename__ = 'users'
    username = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    reset_token = Column(String(250), nullable=True)
    session_id = Column(String(100), nullable=False)
    def __init__(self, *args, **kwargs):
        """Initalizes the users table"""
        super().__init__(*args, **kwargs)
