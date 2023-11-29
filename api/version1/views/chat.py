from flask_socketio import SocketIO, emit, join_room
from cryptography.fernet import Fernet
import uuid
from flask import Flask, request, jsonify
from api.version1.views import app_views

@app_views.on('chat_request')
def handler_req(arg):
    """
    Upcoming updates:
        Handles getting the sending and receiving id
    """