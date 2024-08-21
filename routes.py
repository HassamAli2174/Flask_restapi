from flask import request
from flask_restx import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, session

api = Api()

ns = api.namespace('users', description='User operations')

@ns.route('/register')
class Register(Resource):
    def post(self):
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'message': 'Username and password are required'}, 400

            if session.query(User).filter_by(username=username).first():
                return {'message': 'User already exists'}, 400

            password_hash = generate_password_hash(password)
            new_user = User(username=username, password_hash=password_hash)
            session.add(new_user)
            session.commit()

            return {'message': 'User registered successfully'}, 201

        except Exception as e:
            session.rollback()
            return {'message': str(e)}, 500  # Optionally log the exception or return a custom error message

@ns.route('/login')
class Login(Resource):
    def post(self):
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'message': 'Username and password are required'}, 400

            user = session.query(User).filter_by(username=username).first()
            if not user or not check_password_hash(user.password_hash, password):
                return {'message': 'Invalid credentials'}, 401

            return {'message': 'Login successful'}, 200

        except Exception as e:
            session.rollback()
            return {'message': str(e)}, 500
