from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.models import db, User
from app.utils import validate_email, validate_username, validate_password

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        if not data:
            current_app.logger.warning('Registration attempt with no data provided.')
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields: username, email, password'}), 400
        
        is_valid, msg = validate_username(username)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        try:
            user_count = User.query.count()
            user = User(username=username, email=email)
            user.set_password(password)
            
            if user_count == 0:
                user.role = 'admin'
            
            db.session.add(user)
            db.session.commit()
            
            current_app.logger.info(f'New user registered: {username} (Role: {user.role})')
            
            return jsonify({
                'message': 'User registered successfully',
                'user': user.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error for user {username}: {str(e)}')
            return jsonify({'error': f'Registration failed: {str(e)}'}), 500

    @staticmethod
    def login():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing required fields: username, password'}), 400
        
        try:
            user = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password):
                current_app.logger.info(f'Failed login attempt for username: {username}')
                return jsonify({'error': 'Invalid username or password'}), 401
            
            current_app.logger.info(f'User login successful: {username}')
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        except Exception as e:
            current_app.logger.error(f'Login error for user {username}: {str(e)}')
            return jsonify({'error': f'Login failed: {str(e)}'}), 500

    @staticmethod
    def get_profile():
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({'user': user.to_dict()}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve profile: {str(e)}'}), 500
