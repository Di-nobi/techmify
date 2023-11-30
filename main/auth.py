#!/usr/bin/env python3
"""Authentication File"""
import bcrypt
from main.engine.db import DBStorage
from main.users import MongoDBUser
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
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
    uuid = str(uuid4())
    return uuid

class Auth:
    """Authentication class that interacts with the
    authentication database"""

    def __init__(self):
        self._db = DBStorage()

    def register_user(self, email: str, password: str, username: str,
                      firstname: str, lastname: str):
        """Registers a user to the database"""
        if password is None:
            raise ValueError("Password cannot be None")
        user = self._db.get_user(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        return self._db.add_user(email, _hash_password(password), username, firstname, lastname)
        
    def valid_login(self, email: str, password: str):
        """Validates the password"""
        user = self._db.get_user(email=email)
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode())
    
    def create_session(self, email: str) -> str:
        """Creates a session"""
        user = self._db.get_user(email=email)
        if not user:
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
    def get_user_from_session_id(self, session_id: str):
        """Gets a user from a session id"""
        session_user = self._db.get_user(session_id=session_id)
        if not session_user:
            return None
        return session_user
    
    def get_reset_password_token(self, email: str):
        """Generates a reset password token for a user
        Args:
            email: str
        """
        user = self._db.get_user(email=email)
        if not user:
            raise ValueError
        UUID = _generate_uuid()
        self._db.update_user(user.id, reset_token=UUID)
        return UUID

    def update_password(self, reset_token: str, password: str) -> None:
        """"
        Updates the password of a user
        Args:
            reset_token: string- reset token of an account
            password: str - password of user
        """
        try:
            user = self._db.get_user(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=password,
                             reset_token=None)