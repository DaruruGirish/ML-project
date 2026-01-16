"""
Reddit OAuth 2.0 service for authentication.
"""
import os
import base64
import secrets
import requests
from urllib.parse import urlencode
from flask import session
from src.logger import logging
from src.exception import CustomException
import sys

class RedditOAuthService:
    """Service for handling Reddit OAuth 2.0 flow"""
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_base_url = 'https://www.reddit.com/api/v1/authorize'
        self.token_url = 'https://www.reddit.com/api/v1/access_token'
        self.user_info_url = 'https://oauth.reddit.com/api/v1/me'
        
    def get_authorization_url(self):
        """
        Generate Reddit OAuth authorization URL.
        Returns the URL and stores state in session.
        """
        try:
            # Generate state for CSRF protection
            state = secrets.token_urlsafe(32)
            session['reddit_oauth_state'] = state
            session['reddit_code_verifier'] = secrets.token_urlsafe(32)
            
            params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'state': state,
                'redirect_uri': self.redirect_uri,
                'duration': 'permanent',  # 'temporary' or 'permanent'
                'scope': 'read identity'  # Read posts and get user identity
            }
            
            auth_url = f"{self.auth_base_url}?{urlencode(params)}"
            logging.info("Generated Reddit OAuth authorization URL")
            return auth_url
            
        except Exception as e:
            logging.error(f"Error generating Reddit authorization URL: {str(e)}")
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
            if 'reddit_oauth_state' not in session or session['reddit_oauth_state'] != state:
                raise CustomException("Invalid state parameter", sys)
            
            # Prepare token request
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'User-Agent': 'DetectTheStress/1.0 by YourUsername'  # Reddit requires User-Agent
            }
            
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri
            }
            
            response = requests.post(self.token_url, headers=headers, data=data)
            
            if response.status_code != 200:
                logging.error(f"Token exchange failed: {response.text}")
                raise CustomException(f"Token exchange failed: {response.text}", sys)
            
            token_data = response.json()
            
            # Clean up session
            session.pop('reddit_oauth_state', None)
            session.pop('reddit_code_verifier', None)
            
            logging.info("Successfully exchanged Reddit code for tokens")
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_in': token_data.get('expires_in'),
                'token_type': token_data.get('token_type', 'bearer')
            }
            
        except Exception as e:
            logging.error(f"Error exchanging Reddit code for tokens: {str(e)}")
            raise CustomException(f"Failed to exchange code for tokens: {str(e)}", sys)
    
    def get_user_info(self, access_token):
        """
        Get user information from Reddit API.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            Dictionary with user information
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'User-Agent': 'DetectTheStress/1.0 by YourUsername'
            }
            
            response = requests.get(self.user_info_url, headers=headers)
            
            if response.status_code != 200:
                logging.error(f"Failed to get Reddit user info: {response.text}")
                raise CustomException(f"Failed to get user info: {response.text}", sys)
            
            user_data = response.json()
            
            logging.info(f"Retrieved Reddit user info for: {user_data.get('name')}")
            return {
                'reddit_id': user_data.get('id'),
                'username': user_data.get('name'),
                'display_name': user_data.get('name'),
                'profile_image_url': user_data.get('icon_img', '').replace('&amp;', '&') if user_data.get('icon_img') else None,
                'karma': user_data.get('total_karma', 0),
                'account_created': user_data.get('created_utc')
            }
            
        except Exception as e:
            logging.error(f"Error getting Reddit user info: {str(e)}")
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
                'Authorization': f'Basic {encoded_credentials}',
                'User-Agent': 'DetectTheStress/1.0 by YourUsername'
            }
            
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
            
            response = requests.post(self.token_url, headers=headers, data=data)
            
            if response.status_code != 200:
                logging.error(f"Reddit token refresh failed: {response.text}")
                raise CustomException(f"Token refresh failed: {response.text}", sys)
            
            token_data = response.json()
            logging.info("Successfully refreshed Reddit access token")
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token', refresh_token),
                'expires_in': token_data.get('expires_in')
            }
            
        except Exception as e:
            logging.error(f"Error refreshing Reddit token: {str(e)}")
            raise CustomException(f"Failed to refresh token: {str(e)}", sys)
