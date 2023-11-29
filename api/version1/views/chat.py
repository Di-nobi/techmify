from flask_socketio import SocketIO, emit, join_room
from cryptography.fernet import Fernet
import uuid
from flask import Flask, request, jsonify, abort
from api.version1.views import app_views
from main.engine.db import DBStorage
from main.chatRequest import ChatRequest
from main.users import MongoDBUser
key = Fernet.generate_key()
cipher = Fernet(key)
@app_views.on('chat_request')
def handler_req(arg):
    """
    Upcoming updates:
        Handles getting the sending and receiving id
    """
    try:
        from_id = DBStorage.get(ChatRequest, arg['from_id'])
        if not from_id:
            abort(404)
        to_id = DBStorage.get(ChatRequest, arg['to_id'])
        if not to_id:
            abort(404)
        
        if MongoDBUser.objects(id=to_id):
            ChatRequest(from_id=from_id, to_id=to_id).save()

            emit('chat_request', {'from_id': from_id}, room = to_id)
    except Exception as err:
        print(f"Error occured: {err}")
