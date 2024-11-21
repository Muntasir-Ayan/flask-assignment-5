from flask_restx import Namespace, Resource, fields
from app.utils.auth_utils import token_required, TOKEN_STORAGE

auth_ns = Namespace('auth', description='Authentication operations')

# Request model for token validation
token_model = auth_ns.model('TokenValidation', {
    'token': fields.String(required=True, description='JWT Token')
})

@auth_ns.route('/validate')
class TokenValidation(Resource):
    @auth_ns.expect(token_model)
    def post(self):
        """
        Validate authentication token
        """
        data = auth_ns.payload
        token = data['token']
        
        token_info = TOKEN_STORAGE.get(token)
        if not token_info:
            auth_ns.abort(401, 'Invalid token')
        
        return {
            'message': 'Token is valid',
            'user_id': token_info['user_id'],
            'role': token_info['role']
        }, 200

@auth_ns.route('/roles')
class RoleCheck(Resource):
    @token_required()
    def get(self):
        """
        Check current user's role
        """
        token = request.headers.get('Authorization')
        token_info = TOKEN_STORAGE.get(token)
        
        return {
            'role': token_info['role']
        }, 200