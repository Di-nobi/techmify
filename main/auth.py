#!/usr/bin/env python3
"""Authentication File"""
import bcrypt
from main.engine.db import DBStorage
from main.users import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid5
import jwt

def _hash_password(password: str) -> bytes:
    """Hashes the password and returns it bytes
    Args:
        Passwords"""
    data = password.encode('utf-8')
    return bcrypt.hashpw(data, bcrypt.gensalt())

# def _generate_jwt() -> str:
#     """Generates a JWT token for session, returning a string form"""
#     token = jwt.sign({email, userId: usr_mail._id.toString()}, '4be41d164a4fdeac0fb4be594853f792e16fdc190101f5c89905ae0ce4aee5d9', { expiresIn: '1h' });
#     return token

def _generate_uuid() -> str:
    """Generates a UUID for session authentication"""
    uuid = str(uuid5())
    return uuid

class Auth:
    """Authentication class that interacts with the
    authentication database"""

    def __init__(self):
        self._db = DBStorage()

    def register_user(self, username: str, firstname: str,
                      lastname: str, password: str, email: str):
        """Registers a user to the database"""
        try:
            self._db.get_user(username=username)
            raise ValueError(f"User {username} already exists")
        except NoResultFound:
            return self._db.add_user(username, firstname, lastname, _hash_password(password), email)
        
    def valid_login(self, email: str, password: str):
        """Validates the password"""
        try:
            user = self._db.get_user(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
    
    def create_session(self, email: str) -> str:
        """Creates a session"""
        try:
            user = self._db.get_user(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
    
    def destroy_session(self, user_id):
        """Destroys the session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None