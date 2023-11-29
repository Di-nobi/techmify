#!/usr/bin/env python3
"""Views for the site"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/version1')

from api.version1.views.chat import *