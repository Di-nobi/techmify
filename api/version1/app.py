#!/usr/bin/env python3
"""Flask Application Setup"""
from main import store
from flask import Flask, render_template, jsonify, abort
from flask_cors import CORS
from os import environ
from flask import request
from main.auth import Auth

AUTH = Auth()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """Closes Store"""
    store.close()

@app.errorhandler(404)
def not_found(error):
    """404 error response"""
    return jsonify({'error': 'Not Found'}), 404

@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_users():
    """Registers a user to the database"""
    username = request.form.get('username')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(username, firstname, lastname, password, email)
        return jsonify({"username": user.username, "message": "User Created Successfully"}), 200
    except ValueError:
        return jsonify({"message": "username already exists"}), 400
    
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Logs in a user if the credientials are valid"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = AUTH.valid_login(email, password)
    if not user:
        abort(404)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": f"{email}", "message": "Logged in"})
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    """Main function"""
    host = environ.get('TECH_API_HOST')
    port = environ.get('TECH_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)