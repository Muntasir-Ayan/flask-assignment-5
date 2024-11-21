from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Create API
    api = Api(
        app, 
        version='1.0', 
        title='Travel API', 
        description='A comprehensive Travel Microservices API'
    )

    # Import and register namespaces
    from app.services.destination_service import destination_ns
    from app.services.user_service import user_ns
    from app.services.auth_service import auth_ns

    # Add namespaces to API
    api.add_namespace(destination_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)

    return app