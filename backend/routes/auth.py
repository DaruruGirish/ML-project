"""
Authentication routes for Twitter OAuth, Reddit OAuth, and manual entry.
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for
from backend.models import db, User
from backend.services.twitter_oauth import TwitterOAuthService
from backend.services.reddit_oauth import RedditOAuthService
from backend.config import Config
from src.logger import logging
from src.exception import CustomException
import sys

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/twitter/authorize', methods=['GET'])
def twitter_authorize():
    """Initiate Twitter OAuth flow"""
    try:
        oauth_service = TwitterOAuthService(
            client_id=Config.TWITTER_CLIENT_ID,
            client_secret=Config.TWITTER_CLIENT_SECRET,
            redirect_uri=Config.TWITTER_REDIRECT_URI
        )
        
        auth_url = oauth_service.get_authorization_url()
        return jsonify({
            'status': 'success',
            'auth_url': auth_url
        }), 200
        
    except Exception as e:
        logging.error(f"Error in Twitter authorize: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/twitter/callback', methods=['GET'])
def twitter_callback():
    """Handle Twitter OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error={error}")
        
        if not code or not state:
            return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error=missing_parameters")
        
        oauth_service = TwitterOAuthService(
            client_id=Config.TWITTER_CLIENT_ID,
            client_secret=Config.TWITTER_CLIENT_SECRET,
            redirect_uri=Config.TWITTER_REDIRECT_URI
        )
        
        # Exchange code for tokens
        tokens = oauth_service.exchange_code_for_tokens(code, state)
        
        # Get user info
        user_info = oauth_service.get_user_info(tokens['access_token'])
        
        # Create or update user
        user = User.query.filter_by(twitter_id=user_info['twitter_id']).first()
        
        if user:
            # Update existing user
            user.username = user_info['username']
            user.display_name = user_info['display_name']
            user.profile_image_url = user_info.get('profile_image_url')
            user.access_token = tokens['access_token']  # In production, encrypt this
            user.refresh_token = tokens.get('refresh_token')
            user.is_oauth_connected = True
        else:
            # Create new user
            user = User(
                twitter_id=user_info['twitter_id'],
                username=user_info['username'],
                display_name=user_info['display_name'],
                profile_image_url=user_info.get('profile_image_url'),
                access_token=tokens['access_token'],
                refresh_token=tokens.get('refresh_token'),
                is_oauth_connected=True
            )
            db.session.add(user)
        
        db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['is_authenticated'] = True
        
        logging.info(f"User authenticated: {user.username}")
        
        return redirect(f"{Config.CORS_ORIGINS[0]}/auth/success?user_id={user.id}")
        
    except Exception as e:
        logging.error(f"Error in Twitter callback: {str(e)}")
        return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error={str(e)}")

@auth_bp.route('/manual', methods=['POST'])
def manual_auth():
    """Handle manual username entry"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({
                'status': 'error',
                'message': 'Username is required'
            }), 400
        
        # Remove @ if present
        username = username.lstrip('@')
        
        # Validate username format
        if len(username) < 1 or len(username) > 15:
            return jsonify({
                'status': 'error',
                'message': 'Username must be between 1 and 15 characters'
            }), 400
        
        if not username.replace('_', '').isalnum():
            return jsonify({
                'status': 'error',
                'message': 'Username can only contain letters, numbers, and underscores'
            }), 400
        
        # Check if user exists (for manual entry, we don't require OAuth)
        user = User.query.filter_by(username=username, is_oauth_connected=False).first()
        
        if not user:
            # Create user for manual entry
            user = User(
                username=username,
                is_oauth_connected=False
            )
            db.session.add(user)
            db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['is_authenticated'] = True
        
        logging.info(f"Manual entry authenticated: {username}")
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully connected to @{username}',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Error in manual auth: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'status': 'not_authenticated',
                'authenticated': False
            }), 200
        
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({
                'status': 'not_authenticated',
                'authenticated': False
            }), 200
        
        return jsonify({
            'status': 'authenticated',
            'authenticated': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Error checking auth status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        session.clear()
        return jsonify({
            'status': 'success',
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        logging.error(f"Error in logout: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Reddit OAuth Routes
@auth_bp.route('/reddit/authorize', methods=['GET'])
def reddit_authorize():
    """Initiate Reddit OAuth flow"""
    try:
        oauth_service = RedditOAuthService(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            redirect_uri=Config.REDDIT_REDIRECT_URI
        )
        
        auth_url = oauth_service.get_authorization_url()
        return jsonify({
            'status': 'success',
            'auth_url': auth_url
        }), 200
        
    except Exception as e:
        logging.error(f"Error in Reddit authorize: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/reddit/callback', methods=['GET'])
def reddit_callback():
    """Handle Reddit OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error={error}")
        
        if not code or not state:
            return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error=missing_parameters")
        
        oauth_service = RedditOAuthService(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            redirect_uri=Config.REDDIT_REDIRECT_URI
        )
        
        # Exchange code for tokens
        tokens = oauth_service.exchange_code_for_tokens(code, state)
        
        # Get user info
        user_info = oauth_service.get_user_info(tokens['access_token'])
        
        # Create or update user
        user = User.query.filter_by(reddit_id=user_info['reddit_id']).first()
        
        if user:
            # Update existing user
            user.username = user_info['username']
            user.display_name = user_info['display_name']
            user.profile_image_url = user_info.get('profile_image_url')
            user.reddit_access_token = tokens['access_token']
            user.reddit_refresh_token = tokens.get('refresh_token')
            user.is_reddit_connected = True
            user.reddit_karma = user_info.get('karma', 0)
        else:
            # Check if user exists with same username
            existing_user = User.query.filter_by(username=user_info['username']).first()
            if existing_user:
                # Update existing user with Reddit info
                existing_user.reddit_id = user_info['reddit_id']
                existing_user.reddit_access_token = tokens['access_token']
                existing_user.reddit_refresh_token = tokens.get('refresh_token')
                existing_user.is_reddit_connected = True
                existing_user.reddit_karma = user_info.get('karma', 0)
                user = existing_user
            else:
                # Create new user
                user = User(
                    reddit_id=user_info['reddit_id'],
                    username=user_info['username'],
                    display_name=user_info['display_name'],
                    profile_image_url=user_info.get('profile_image_url'),
                    reddit_access_token=tokens['access_token'],
                    reddit_refresh_token=tokens.get('refresh_token'),
                    is_reddit_connected=True,
                    reddit_karma=user_info.get('karma', 0)
                )
                db.session.add(user)
        
        db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['is_authenticated'] = True
        
        logging.info(f"Reddit user authenticated: {user.username}")
        
        return redirect(f"{Config.CORS_ORIGINS[0]}/auth/success?user_id={user.id}&platform=reddit")
        
    except Exception as e:
        logging.error(f"Error in Reddit callback: {str(e)}")
        return redirect(f"{Config.CORS_ORIGINS[0]}/auth/error?error={str(e)}")

@auth_bp.route('/reddit/manual', methods=['POST'])
def reddit_manual():
    """Handle manual Reddit username entry"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({
                'status': 'error',
                'message': 'Username is required'
            }), 400
        
        # Remove u/ if present
        username = username.replace('u/', '').replace('/u/', '').strip()
        
        # Validate username format (Reddit usernames: 3-20 chars, alphanumeric and underscores)
        if len(username) < 3 or len(username) > 20:
            return jsonify({
                'status': 'error',
                'message': 'Reddit username must be between 3 and 20 characters'
            }), 400
        
        if not username.replace('_', '').isalnum():
            return jsonify({
                'status': 'error',
                'message': 'Reddit username can only contain letters, numbers, and underscores'
            }), 400
        
        # Check if user exists
        user = User.query.filter_by(username=username, is_reddit_connected=False).first()
        
        if not user:
            # Create user for manual entry
            user = User(
                username=username,
                is_reddit_connected=False
            )
            db.session.add(user)
            db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['is_authenticated'] = True
        
        logging.info(f"Manual Reddit entry authenticated: {username}")
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully connected to u/{username}',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Error in Reddit manual auth: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
