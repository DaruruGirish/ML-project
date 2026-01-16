"""
Twitter/X OAuth 2.0 service for authentication.
"""
import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import urlencode, parse_qs
from flask import session, url_for
from src.logger import logging
from src.exception import CustomException
import sys

class TwitterOAuthService:
    """Service for handling Twitter/X OAuth 2.0 flow"""
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_base_url = 'https://twitter.com/i/oauth2/authorize'
        self.token_url = 'https://api.twitter.com/2/oauth2/token'
        self.user_info_url = 'https://api.twitter.com/2/users/me'
        
    def generate_code_verifier(self):
        """Generate PKCE code verifier"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
    def generate_code_challenge(self, verifier):
        """Generate PKCE code challenge from verifier"""
        challenge = hashlib.sha256(verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
    
    def get_authorization_url(self):
        """
        Generate Twitter OAuth authorization URL with PKCE.
        Returns the URL and stores code_verifier in session.
        """
        try:
            code_verifier = self.generate_code_verifier()
            code_challenge = self.generate_code_challenge(code_verifier)
            
            # Store in session for later verification
            session['oauth_code_verifier'] = code_verifier
            session['oauth_state'] = secrets.token_urlsafe(32)
            
            params = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'scope': 'tweet.read users.read offline.access',
                'state': session['oauth_state'],
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256'
            }
            
            auth_url = f"{self.auth_base_url}?{urlencode(params)}"
            logging.info("Generated Twitter OAuth authorization URL")
            return auth_url
            
        except Exception as e:
            logging.error(f"Error generating authorization URL: {str(e)}")
            raise CustomException(f"Failed to generate authorization URL: {str(e)}", sys)
    
    def exchange_code_for_tokens(self, code, state):
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            code: Authorization code from callback
            state: State parameter for CSRF protection
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        try:
            # Verify state
            if 'oauth_state' not in session or session['oauth_state'] != state:
                raise CustomException("Invalid state parameter", sys)
            
            code_verifier = session.get('oauth_code_verifier')
            if not code_verifier:
                raise CustomException("Code verifier not found in session", sys)
            
            # Prepare token request
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            data = {
                'code': code,
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'code_verifier': code_verifier
            }
            
            response = requests.post(self.token_url, headers=headers, data=data)
            
            if response.status_code != 200:
                logging.error(f"Token exchange failed: {response.text}")
                raise CustomException(f"Token exchange failed: {response.text}", sys)
            
            token_data = response.json()
            
            # Clean up session
            session.pop('oauth_code_verifier', None)
            session.pop('oauth_state', None)
            
            logging.info("Successfully exchanged code for tokens")
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_in': token_data.get('expires_in'),
                'token_type': token_data.get('token_type', 'bearer')
            }
            
        except Exception as e:
            logging.error(f"Error exchanging code for tokens: {str(e)}")
            raise CustomException(f"Failed to exchange code for tokens: {str(e)}", sys)
    
    def get_user_info(self, access_token):
        """
        Get user information from Twitter API.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            Dictionary with user information
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            params = {
                'user.fields': 'id,username,name,profile_image_url,description'
            }
            
            response = requests.get(self.user_info_url, headers=headers, params=params)
            
            if response.status_code != 200:
                logging.error(f"Failed to get user info: {response.text}")
                raise CustomException(f"Failed to get user info: {response.text}", sys)
            
            data = response.json()
            user_data = data.get('data', {})
            
            logging.info(f"Retrieved user info for: {user_data.get('username')}")
            return {
                'twitter_id': user_data.get('id'),
                'username': user_data.get('username'),
                'display_name': user_data.get('name'),
                'profile_image_url': user_data.get('profile_image_url'),
                'description': user_data.get('description')
            }
            
        except Exception as e:
            logging.error(f"Error getting user info: {str(e)}")
            raise CustomException(f"Failed to get user info: {str(e)}", sys)
    
    def refresh_access_token(self, refresh_token):
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: OAuth refresh token
            
        Returns:
            Dictionary with new access_token
        """
        try:
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            data = {
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
                'client_id': self.client_id
            }
            
            response = requests.post(self.token_url, headers=headers, data=data)
            
            if response.status_code != 200:
                logging.error(f"Token refresh failed: {response.text}")
                raise CustomException(f"Token refresh failed: {response.text}", sys)
            
            token_data = response.json()
            logging.info("Successfully refreshed access token")
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token', refresh_token),
                'expires_in': token_data.get('expires_in')
            }
            
        except Exception as e:
            logging.error(f"Error refreshing token: {str(e)}")
            raise CustomException(f"Failed to refresh token: {str(e)}", sys)
