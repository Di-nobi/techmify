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
        from_id = DBStorage.get(ChatRequest, arg['from_id'])
        if not from_id:
            abort(404)
        # Gets the senders Id from the database
        to_id = DBStorage.get(ChatRequest, arg['to_id'])
        if not to_id:
            abort(404)
        
        if MongoDBUser.objects(id=to_id):
            ChatRequest(from_id=from_id, to_id=to_id).save()

            emit('chat_request', {'from_id': from_id}, room = to_id)
    except Exception as err:
        print(f"Error occured: {err}")

@socketio.on('accept_request')
def accepts_reg(data):
    """This functions handles accepting of a users request"""

    # Gets the receivers Id from the database
    to_id = DBStorage.get(ChatRequest, data['to_id'])
    if not to_id:
        abort(404)
    # Gets the senders Id from the database
    from_id = DBStorage.get(ChatRequest, data['from_id'])
    if not from_id:
        abort(404)
    
    room = str(uuid4())

    #Displays to both the sender and the receiver that the chat has been accepted
    emit('chat_accepted', {'room': room}, room=from_id)
    emit('chat_accepted', {'room': room}, room=to_id)

    #Adds the sender and the receiver to thesame room
    join_room(room, sid=from_id)
    join_room(room, sid=to_id)

@socketio.on('message')
def message_handler(args):
    """This handles the conversation between users in the room"""

    #Decrypts the message for the user to see on the clients interface
    message_decrypt = cipher.decrypt(args['message'].encode()).decode()

    #Stores the Encrypted message to the backend server for security
    Message(content=args['message'], room=args['room']).save()

    #Displays the messages
    emit('message', {'message': message_decrypt}, room=args['room'])
