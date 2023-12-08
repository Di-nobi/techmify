import mongoengine

class ChatRequest(mongoengine.EmbeddedDocument):
    from_id = mongoengine.StringField(required=True)
    to_id = mongoengine.StringField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'chatRequest'
    }