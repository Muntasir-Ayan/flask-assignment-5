from flask import request
from flask_restx import Namespace, Resource, fields
from app.utils.auth_utils import generate_token, hash_password, verify_password, token_required
from app.utils.validators import validate_email
import uuid

user_ns = Namespace('users', description='User management operations')

# In-memory storage for users
USERS = {}

# Request/Response Models
user_model = user_ns.model('User', {
    'id': fields.String(readonly=True, description='User unique identifier'),
    'name': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User email address'),
    'role': fields.String(enum=['User', 'Admin'], description='User role')
})

user_input_model = user_ns.model('UserInput', {
    'name': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(enum=['User', 'Admin'], description='User role')
})

@user_ns.route('')
class UserList(Resource):
    @token_required(roles=['Admin'])
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """List all users (Admin only)"""
        return list(USERS.values())

    @user_ns.expect(user_input_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """Register a new user"""
        data = request.json
        
        # Validate input
        if not validate_email(data['email']):
            user_ns.abort(400, 'Invalid email format')
        
        # Check if user exists
        if any(user['email'] == data['email'] for user in USERS.values()):
            user_ns.abort(409, 'Email already registered')
        
        # Create user
        user_id = str(uuid.uuid4())
        new_user = {
            'id': user_id,
            'name': data['name'],
            'email': data['email'],
            'password': hash_password(data['password']),
            'role': data.get('role', 'User')
        }
        
        USERS[user_id] = new_user
        
        return new_user, 201

@user_ns.route('/<string:user_id>')
class UserResource(Resource):
    @token_required()
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        """Get user profile"""
        user = USERS.get(user_id)
        if not user:
            user_ns.abort(404, 'User not found')
        return user

    @token_required()
    @user_ns.expect(user_input_model)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        """Update user profile"""
        user = USERS.get(user_id)
        if not user:
            user_ns.abort(404, 'User not found')
        
        data = request.json
        
        if 'name' in data:
            user['name'] = data['name']
        
        if 'email' in data:
            if not validate_email(data['email']):
                user_ns.abort(400, 'Invalid email format')
            user['email'] = data['email']
        
        return user

@user_ns.route('/login')
class UserLogin(Resource):
    def post(self):
        """User login and generate token"""
        data = request.json
        
        # Find user by email
        user = next((u for u in USERS.values() if u['email'] == data['email']), None)
        
        if user and verify_password(user['password'], data['password']):
            token = generate_token(user['id'], user['role'])
            return {
                'token': token,
                'user': user
            }
        
        user_ns.abort(401, 'Invalid credentials')