"""
Resources routes for mental health content.
"""
from flask import Blueprint, request, jsonify
from backend.models import db, Resource
from src.logger import logging
from src.exception import CustomException
import sys

resources_bp = Blueprint('resources', __name__, url_prefix='/api/resources')

@resources_bp.route('/', methods=['GET'])
def get_resources():
    """Get all active resources, optionally filtered by type"""
    try:
        resource_type = request.args.get('type')  # 'blog', 'wikipedia', 'game', etc.
        category = request.args.get('category')  # 'audio', 'writing', 'practice', etc.
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        
        query = Resource.query.filter_by(is_active=True)
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        
        if category:
            query = query.filter_by(category=category)
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        resources = query.order_by(Resource.created_at.desc()).all()
        
        return jsonify({
            'status': 'success',
            'resources': [resource.to_dict() for resource in resources]
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting resources: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@resources_bp.route('/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get specific resource by ID"""
    try:
        resource = Resource.query.get(resource_id)
        
        if not resource or not resource.is_active:
            return jsonify({
                'status': 'error',
                'message': 'Resource not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'resource': resource.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting resource: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@resources_bp.route('/types', methods=['GET'])
def get_resource_types():
    """Get list of available resource types"""
    try:
        types = db.session.query(Resource.resource_type).distinct().all()
        types_list = [t[0] for t in types if t[0]]
        
        return jsonify({
            'status': 'success',
            'types': types_list
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting resource types: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@resources_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get list of available categories"""
    try:
        categories = db.session.query(Resource.category).distinct().all()
        categories_list = [c[0] for c in categories if c[0]]
        
        return jsonify({
            'status': 'success',
            'categories': categories_list
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting categories: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
