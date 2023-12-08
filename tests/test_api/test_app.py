import unittest
from unittest.mock import patch, MagicMock
from flask_socketio import SocketIO
from api.version1.app import app  # Assuming your Flask app is named 'app'
from api.version1.views import socketio
from main.users import MongoDBUser
from main.chatRequest import ChatRequest
from main.chats import Message
import time

class TestSocketHandlers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.socketio_client = SocketIO(app, logger=False, engineio_logger=False).test_client(self.app)
        self.socketio_client.connect()
    def tearDown(self):
        self.socketio_client.disconnect()

    @patch('api.version1.views.MongoDBUser.objects')
    def test_handler_req(self, mock_mongo_objects):
        # Mock MongoDBUser.objects
        mock_mongo_objects.return_value = MagicMock()

        # Simulate a chat_request event
        data = {'from_id': 'user1', 'to_id': 'user2'}
        self.socketio_client.emit('chat_request', data)

        # Assert that MongoDBUser.objects was called with the correct parameters
        mock_mongo_objects.assert_called_once_with(username=data['from_id'])
        
        # Assert that the 'chat_request' event was emitted
        received_data = self.socketio_client.get_received()
        self.assertEqual(received_data[0]['name'], 'chat_request')

    @patch('api.version1.views.MongoDBUser.objects')
    def test_accepts_reg(self, mock_mongo_objects):
        # Mock MongoDBUser.objects
        mock_mongo_objects.return_value = MagicMock()

        # Simulate an accept_request event
        data = {'from_id': 'user1', 'to_id': 'user2'}
        self.socketio_client.emit('accept_request', data)

        # Assert that MongoDBUser.objects was called with the correct parameters
        mock_mongo_objects.assert_called_once_with(username=data['to_id'])
        
        # Assert that the 'chat_accepted' event was emitted
        received_data = self.socketio_client.get_received()
        self.assertEqual(received_data[0]['name'], 'chat_accepted')

    def test_message_handler(self):
        # Simulate a message event
        data = {'message': 'Hello!', 'room': 'room1'}
        self.socketio_client.emit('message', data)
        time.sleep(0.1)

        # Assert that the 'message' event was emitted
        # received_data = self.socketio_client.get_received()
        # self.assertEqual(received_data[0]['name'], 'message')

if __name__ == '__main__':
    unittest.main()
