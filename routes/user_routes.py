from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from db.user_db import insert_user, find_user_by_name

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = {
        "user_id": data['user_id'],
        "user_name": data['user_name'],
        "password": generate_password_hash(data['password'])
    }
    insert_user(user)
    return jsonify({"msg": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = find_user_by_name(data['user_name'])
    if user and check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=user['user_id'])
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401
