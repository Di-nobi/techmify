import mongoengine

class ChatRequest(mongoengine.Document):
    from_id = mongoengine.StringField(required=True)
    to_id = mongoengine.StringField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'chatRequest'
    }