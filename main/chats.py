import mongoengine

class Message(mongoengine.Document):
    contents = mongoengine.StringField(required=True)
    the_room = mongoengine.StringField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'chats'
    }