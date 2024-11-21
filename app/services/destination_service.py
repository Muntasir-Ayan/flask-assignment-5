from flask import request
from flask_restx import Namespace, Resource, fields
from app.utils.auth_utils import token_required
import uuid

destination_ns = Namespace('destinations', description='Destination management operations')

# In-memory storage for destinations
DESTINATIONS = {
    "1": {
        "id": "1",
        "name": "Eiffel Tower",
        "description": "A wrought-iron lattice tower in Paris, France.",
        "location": "Paris, France"
    },
    "2": {
        "id": "2",
        "name": "Grand Canyon",
        "description": "A steep-sided canyon carved by the Colorado River.",
        "location": "Arizona, USA"
    },
    "3": {
        "id": "3",
        "name": "Great Wall of China",
        "description": "A historic wall built to protect Chinese states and empires.",
        "location": "China"
    }
}

# Request/Response Models
destination_model = destination_ns.model('Destination', {
    'id': fields.String(readonly=True, description='Destination unique identifier'),
    'name': fields.String(required=True, description='Destination name'),
    'description': fields.String(description='Destination description'),
    'location': fields.String(required=True, description='Destination location')
})

destination_input_model = destination_ns.model('DestinationInput', {
    'name': fields.String(required=True, description='Destination name'),
    'description': fields.String(description='Destination description'),
    'location': fields.String(required=True, description='Destination location')
})

@destination_ns.route('')
class DestinationList(Resource):
    @destination_ns.marshal_list_with(destination_model)
    def get(self):
        """List all destinations"""
        return list(DESTINATIONS.values())

    @token_required(roles=['Admin'])
    @destination_ns.expect(destination_input_model)
    @destination_ns.marshal_with(destination_model, code=201)
    def post(self):
        """Create a new destination (Admin only)"""
        data = request.json
        
        destination_id = str(uuid.uuid4())
        new_destination = {
            'id': destination_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'location': data['location']
        }
        
        DESTINATIONS[destination_id] = new_destination
        
        return new_destination, 201

@destination_ns.route('/<string:destination_id>')
class DestinationResource(Resource):
    @destination_ns.marshal_with(destination_model)
    def get(self, destination_id):
        """Get a specific destination"""
        destination = DESTINATIONS.get(destination_id)
        if not destination:
            destination_ns.abort(404, 'Destination not found')
        return destination

    @token_required(roles=['Admin'])
    @destination_ns.expect(destination_input_model)
    @destination_ns.marshal_with(destination_model)
    def put(self, destination_id):
        """Update a destination (Admin only)"""
        destination = DESTINATIONS.get(destination_id)
        if not destination:
            destination_ns.abort(404, 'Destination not found')
        
        data = request.json
        
        if 'name' in data:
            destination['name'] = data['name']
        if 'description' in data:
            destination['description'] = data['description']
        if 'location' in data:
            destination['location'] = data['location']
        
        return destination

    @token_required(roles=['Admin'])
    def delete(self, destination_id):
        """Delete a destination (Admin only)"""
        destination = DESTINATIONS.get(destination_id)
        if not destination:
            destination_ns.abort(404, 'Destination not found')
        
        del DESTINATIONS[destination_id]
        
        return {'message': 'Destination deleted successfully'}, 200