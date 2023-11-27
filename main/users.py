import mongoengine
import datetime

class MongoDBUser(mongoengine.Document):
    # id = mongoengine.IntField(required=False)
    email = mongoengine.StringField(required=True)
    hashed_password = mongoengine.StringField(required=True)
    reset_token= mongoengine.StringField(required=False)
    session_id = mongoengine.StringField(required=False)

    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
