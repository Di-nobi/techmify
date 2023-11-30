#!/usr/bin/env python3
"""Flask Application Setup"""
# from main import store
from flask import Flask, render_template, jsonify, abort, redirect
from flask_cors import CORS
from os import environ
from flask import request
# from api.version1.views import app_views
from main.auth import Auth
from flask_socketio import SocketIO, emit, join_room


AUTH = Auth()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# app.register_blueprint(app_views)
# socketio = SocketIO(app)
# @app.teardown_appcontext
# def close_db(error):
#     """Closes Store"""
#     store.close()

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
    
    if email is None or password is None:
        return jsonify({"message": "Email and password are required"}), 400
    try:
        user = AUTH.register_user(email, password, username, firstname, lastname)
        return jsonify({"email": user.email, "message": "User Created Successfully"}), 200
    except ValueError:
        return jsonify({"message": "email already exists"}), 400
    
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

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logouts out a user by deleting current session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(404)
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile():
    """Gets the profile of a user"""
    session = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_token():
    """
    Gets a reset password token for a user
    """
    email = request.form.get("email")
    user = AUTH.get_reset_password_token(email)
    if not user:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{user}"}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Updates password of a user """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        user = AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "message": "Password updated"}), 200

if __name__ == "__main__":
    """Main function"""
    host = environ.get('TECH_API_HOST')
    port = environ.get('TECH_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
    # socketio.run(app)