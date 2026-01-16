"""
Twitter API service for fetching tweets and user data.
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.logger import logging
from src.exception import CustomException
import sys

class TwitterAPIService:
    """Service for interacting with Twitter API v2"""
    
    def __init__(self, bearer_token: Optional[str] = None):
        self.bearer_token = bearer_token
        self.base_url = 'https://api.twitter.com/2'
        self.headers = {}
        if bearer_token:
            self.headers['Authorization'] = f'Bearer {bearer_token}'
    
    def set_access_token(self, access_token: str):
        """Set OAuth access token for authenticated requests"""
        self.headers['Authorization'] = f'Bearer {access_token}'
    
    def get_user_by_username(self, username: str) -> Dict:
        """
        Get user information by username.
        
        Args:
            username: Twitter username (without @)
            
        Returns:
            Dictionary with user information
        """
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            url = f"{self.base_url}/users/by/username/{username}"
            params = {
                'user.fields': 'id,username,name,profile_image_url,description,public_metrics,created_at'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 404:
                raise CustomException(f"User @{username} not found", sys)
            elif response.status_code != 200:
                logging.error(f"Failed to get user: {response.text}")
                raise CustomException(f"Failed to get user: {response.text}", sys)
            
            data = response.json()
            return data.get('data', {})
            
        except CustomException:
            raise
        except Exception as e:
            logging.error(f"Error getting user by username: {str(e)}")
            raise CustomException(f"Failed to get user: {str(e)}", sys)
    
    def get_user_tweets(self, user_id: str, max_results: int = 100, 
                       start_time: Optional[datetime] = None) -> List[Dict]:
        """
        Get recent tweets from a user.
        
        Args:
            user_id: Twitter user ID
            max_results: Maximum number of tweets to fetch (max 100)
            start_time: Start time for tweet search (default: 30 days ago)
            
        Returns:
            List of tweet dictionaries
        """
        try:
            if start_time is None:
                start_time = datetime.utcnow() - timedelta(days=30)
            
            url = f"{self.base_url}/users/{user_id}/tweets"
            params = {
                'max_results': min(max_results, 100),
                'start_time': start_time.isoformat() + 'Z',
                'tweet.fields': 'id,text,created_at,public_metrics,lang',
                'exclude': 'retweets,replies'  # Focus on original tweets
            }
            
            all_tweets = []
            next_token = None
            
            while len(all_tweets) < max_results:
                if next_token:
                    params['pagination_token'] = next_token
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    logging.error(f"Failed to get tweets: {response.text}")
                    break
                
                data = response.json()
                tweets = data.get('data', [])
                all_tweets.extend(tweets)
                
                # Check for pagination
                meta = data.get('meta', {})
                next_token = meta.get('next_token')
                
                if not next_token or len(all_tweets) >= max_results:
                    break
            
            logging.info(f"Retrieved {len(all_tweets)} tweets for user {user_id}")
            return all_tweets[:max_results]
            
        except Exception as e:
            logging.error(f"Error getting user tweets: {str(e)}")
            raise CustomException(f"Failed to get tweets: {str(e)}", sys)
    
    def get_tweets_by_username(self, username: str, max_results: int = 100,
                               lookback_days: int = 30) -> List[Dict]:
        """
        Get tweets by username (convenience method).
        
        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets to fetch
            lookback_days: Number of days to look back
            
        Returns:
            List of tweet dictionaries
        """
        try:
            # Get user info first
            user_info = self.get_user_by_username(username)
            user_id = user_info.get('id')
            
            if not user_id:
                raise CustomException(f"Could not get user ID for @{username}", sys)
            
            # Calculate start time
            start_time = datetime.utcnow() - timedelta(days=lookback_days)
            
            # Get tweets
            tweets = self.get_user_tweets(user_id, max_results, start_time)
            
            return tweets
            
        except CustomException:
            raise
        except Exception as e:
            logging.error(f"Error getting tweets by username: {str(e)}")
            raise CustomException(f"Failed to get tweets: {str(e)}", sys)
