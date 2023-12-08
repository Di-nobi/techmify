import mongoengine
import datetime
from main.chats import Message
from main.chatRequest import ChatRequest

class MongoDBUser(mongoengine.Document):
    # _id = mongoengine.StringField(required=False)
    username = mongoengine.StringField(required=True)
    firstname = mongoengine.StringField(required=False)
    lastname = mongoengine.StringField(required=False)
    email = mongoengine.StringField(required=True)
    hashed_password = mongoengine.StringField(required=True)
    reset_token= mongoengine.StringField(required=False)
    session_id = mongoengine.StringField(required=False)

    message = mongoengine.EmbeddedDocumentListField(Message)
    chat_request = mongoengine.EmbeddedDocumentListField(ChatRequest)
    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
