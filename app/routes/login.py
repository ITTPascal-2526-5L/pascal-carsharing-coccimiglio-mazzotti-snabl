from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import check_password_hash
import json
import os

login_bp = Blueprint("login", __name__, url_prefix="/api")

@login_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Determine filenames based on testing config
        testing = bool(current_app.config.get('TESTING'))
        drivers_file = 'test_drivers.json' if testing else 'drivers.json'
        passengers_file = 'test_passengers.json' if testing else 'passengers.json'

        user_found = None
        role = None

        # Check drivers
        if os.path.exists(drivers_file):
            with open(drivers_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            user = json.loads(line)
                            if user.get('username') == username:
                                user_found = user
                                role = 'driver'
                                break
                        except json.JSONDecodeError:
                            continue

        # Check passengers if not found in drivers
        if not user_found and os.path.exists(passengers_file):
            with open(passengers_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            user = json.loads(line)
                            if user.get('username') == username:
                                user_found = user
                                role = 'passenger'
                                break
                        except json.JSONDecodeError:
                            continue

        if not user_found:
            return jsonify({'error': 'Invalid username or password'}), 401

        #use check_password_hash
        if not check_password_hash(user_found.get('password'), password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Return user info (excluding password) and access token
        user_data = user_found.copy()
        user_data.pop('password', None)
        user_data['role'] = role

        access_token = create_access_token(identity=username, additional_claims={"role": role})

        return jsonify({
            'message': 'Login successful',
            'user': user_data,
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@login_bp.route("/logout", methods=["POST"])
def logout():
    try:
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@login_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    try:
        current_user_identity = get_jwt_identity()
        current_user_claims = get_jwt()
        return jsonify({
            'message': 'Access granted',
            'user_identity': current_user_identity,
            'user_claims': current_user_claims
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

