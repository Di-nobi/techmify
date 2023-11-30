#!/usr/bin/env python3
"""Views for the site"""
from flask import Blueprint
from flask_socketio import SocketIO

socketio = SocketIO(message_queue="redis://")
app_views = Blueprint('app_views', __name__)

from api.version1.views.chat import *