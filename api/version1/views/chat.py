from flask_socketio import SocketIO, emit, join_room
from cryptography.fernet import Fernet
import uuid
from flask import Flask, request, jsonify, abort
from api.version1.views import socketio, app_views
from main.engine.db import DBStorage
from main.chatRequest import ChatRequest
from main.chats import Message
from main.users import MongoDBUser
from uuid import uuid4
key = Fernet.generate_key()
cipher = Fernet(key)

@socketio.on('chat_request')
def handler_req(arg):
    """
    Upcoming updates:
        Handles getting the sending and receiving id
    """
    try:
        # Gets the receivers Id from the database
        from_id = MongoDBUser.objects(username=arg['from_id']).first()
        if not from_id:
            abort(404)
        # Gets the senders Id from the database
        to_id = MongoDBUser.objects(username=arg['to_id']).first()
        if not to_id:
            abort(404)
        
        chat_req = ChatRequest(from_id=from_id.username, to_id=to_id.username)
        from_id.chat_request.append(chat_req)
        from_id.save()

        to_chat_req = ChatRequest(from_id=from_id.username, to_id=to_id.username)
        to_id.chat_request.append(to_chat_req)
        to_id.save()
        emit('chat_request', {'from_id': from_id}, room = to_id)
    except Exception as err:
        print(f"Error occured: {err}")

@socketio.on('accept_request')
def accepts_reg(data):
    """This functions handles accepting of a users request"""

    # Gets the receivers Id from the database
    to_id = MongoDBUser.objects(username=data['to_id']).first()
    if not to_id:
        abort(404)
    # Gets the senders Id from the database
    from_id = MongoDBUser.objects(username=data['from_id']).first()
    if not from_id:
        abort(404)
    
    room = str(uuid4())

    emit('chat_accepted', {'room': room}, room=from_id)
    emit('chat_accepted', {'room': room}, room=to_id)

    join_room(room, sid=from_id)
    join_room(room, sid=to_id)

@socketio.on('message')
def message_handler(args):
    """This handles the conversation between users in the room"""

    message_decrypt = cipher.decrypt(args['message'].encode()).decode()

    Message(content=args['message'], room=args['room']).save()

    emit('message', {'message': message_decrypt}, room=args['room'])
