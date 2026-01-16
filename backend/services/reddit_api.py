"""
Reddit API service for fetching posts and comments.
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.logger import logging
from src.exception import CustomException
import sys

class RedditAPIService:
    """Service for interacting with Reddit API"""
    
    def __init__(self, access_token: Optional[str] = None, user_agent: str = 'DetectTheStress/1.0'):
        self.access_token = access_token
        self.user_agent = user_agent
        self.base_url = 'https://oauth.reddit.com' if access_token else 'https://www.reddit.com'
        self.headers = {
            'User-Agent': user_agent
        }
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'
    
    def set_access_token(self, access_token: str):
        """Set OAuth access token for authenticated requests"""
        self.access_token = access_token
        self.base_url = 'https://oauth.reddit.com'
        self.headers['Authorization'] = f'Bearer {access_token}'
    
    def get_user_by_username(self, username: str) -> Dict:
        """
        Get user information by username.
        
        Args:
            username: Reddit username (without u/)
            
        Returns:
            Dictionary with user information
        """
        try:
            # Remove u/ if present
            username = username.replace('u/', '').replace('/u/', '').strip()
            
            url = f"{self.base_url}/user/{username}/about.json"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 404:
                raise CustomException(f"User u/{username} not found", sys)
            elif response.status_code != 200:
                logging.error(f"Failed to get Reddit user: {response.text}")
                raise CustomException(f"Failed to get user: {response.text}", sys)
            
            data = response.json()
            user_data = data.get('data', {})
            
            return {
                'id': user_data.get('id'),
                'username': user_data.get('name'),
                'display_name': user_data.get('name'),
                'profile_image_url': user_data.get('icon_img', '').replace('&amp;', '&') if user_data.get('icon_img') else None,
                'karma': user_data.get('total_karma', 0),
                'account_created': user_data.get('created_utc'),
                'subreddit': user_data.get('subreddit', {})
            }
            
        except CustomException:
            raise
        except Exception as e:
            logging.error(f"Error getting Reddit user by username: {str(e)}")
            raise CustomException(f"Failed to get user: {str(e)}", sys)
    
    def get_user_posts(self, username: str, limit: int = 100, 
                      sort: str = 'new', time_filter: str = 'all') -> List[Dict]:
        """
        Get recent posts from a user.
        
        Args:
            username: Reddit username (without u/)
            limit: Maximum number of posts to fetch (max 100)
            sort: Sort order ('hot', 'new', 'top', 'controversial')
            time_filter: Time filter for 'top' and 'controversial' ('hour', 'day', 'week', 'month', 'year', 'all')
            
        Returns:
            List of post dictionaries
        """
        try:
            # Remove u/ if present
            username = username.replace('u/', '').replace('/u/', '').strip()
            
            url = f"{self.base_url}/user/{username}/submitted.json"
            params = {
                'limit': min(limit, 100),
                'sort': sort
            }
            
            if sort in ['top', 'controversial']:
                params['t'] = time_filter
            
            all_posts = []
            after = None
            
            while len(all_posts) < limit:
                if after:
                    params['after'] = after
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    logging.error(f"Failed to get Reddit posts: {response.text}")
                    break
                
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                if not posts:
                    break
                
                # Extract post data
                for post_wrapper in posts:
                    post_data = post_wrapper.get('data', {})
                    all_posts.append({
                        'id': post_data.get('id'),
                        'title': post_data.get('title', ''),
                        'selftext': post_data.get('selftext', ''),
                        'text': post_data.get('selftext', ''),  # Alias for consistency
                        'created_utc': post_data.get('created_utc'),
                        'created_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat() if post_data.get('created_utc') else None,
                        'subreddit': post_data.get('subreddit', ''),
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'url': post_data.get('url', ''),
                        'permalink': f"https://reddit.com{post_data.get('permalink', '')}",
                        'is_self': post_data.get('is_self', False),
                        'link_flair_text': post_data.get('link_flair_text'),
                    })
                
                # Check for pagination
                after = data.get('data', {}).get('after')
                if not after or len(all_posts) >= limit:
                    break
            
            logging.info(f"Retrieved {len(all_posts)} Reddit posts for user {username}")
            return all_posts[:limit]
            
        except Exception as e:
            logging.error(f"Error getting Reddit user posts: {str(e)}")
            raise CustomException(f"Failed to get posts: {str(e)}", sys)
    
    def get_user_comments(self, username: str, limit: int = 100,
                         sort: str = 'new') -> List[Dict]:
        """
        Get recent comments from a user.
        
        Args:
            username: Reddit username (without u/)
            limit: Maximum number of comments to fetch (max 100)
            sort: Sort order ('top', 'new', 'controversial', 'old')
            
        Returns:
            List of comment dictionaries
        """
        try:
            # Remove u/ if present
            username = username.replace('u/', '').replace('/u/', '').strip()
            
            url = f"{self.base_url}/user/{username}/comments.json"
            params = {
                'limit': min(limit, 100),
                'sort': sort
            }
            
            all_comments = []
            after = None
            
            while len(all_comments) < limit:
                if after:
                    params['after'] = after
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    logging.error(f"Failed to get Reddit comments: {response.text}")
                    break
                
                data = response.json()
                comments = data.get('data', {}).get('children', [])
                
                if not comments:
                    break
                
                # Extract comment data
                for comment_wrapper in comments:
                    comment_data = comment_wrapper.get('data', {})
                    all_comments.append({
                        'id': comment_data.get('id'),
                        'text': comment_data.get('body', ''),
                        'created_utc': comment_data.get('created_utc'),
                        'created_at': datetime.fromtimestamp(comment_data.get('created_utc', 0)).isoformat() if comment_data.get('created_utc') else None,
                        'subreddit': comment_data.get('subreddit', ''),
                        'score': comment_data.get('score', 0),
                        'post_id': comment_data.get('link_id', '').replace('t3_', ''),
                        'permalink': f"https://reddit.com{comment_data.get('permalink', '')}",
                    })
                
                # Check for pagination
                after = data.get('data', {}).get('after')
                if not after or len(all_comments) >= limit:
                    break
            
            logging.info(f"Retrieved {len(all_comments)} Reddit comments for user {username}")
            return all_comments[:limit]
            
        except Exception as e:
            logging.error(f"Error getting Reddit user comments: {str(e)}")
            raise CustomException(f"Failed to get comments: {str(e)}", sys)
    
    def get_user_content(self, username: str, include_comments: bool = True,
                        max_posts: int = 50, max_comments: int = 50) -> List[Dict]:
        """
        Get both posts and comments from a user.
        
        Args:
            username: Reddit username
            include_comments: Whether to include comments
            max_posts: Maximum posts to fetch
            max_comments: Maximum comments to fetch
            
        Returns:
            Combined list of posts and comments
        """
        try:
            all_content = []
            
            # Get posts
            posts = self.get_user_posts(username, limit=max_posts)
            for post in posts:
                post['content_type'] = 'post'
                all_content.append(post)
            
            # Get comments if requested
            if include_comments:
                comments = self.get_user_comments(username, limit=max_comments)
                for comment in comments:
                    comment['content_type'] = 'comment'
                    all_content.append(comment)
            
            # Sort by creation time (newest first)
            all_content.sort(key=lambda x: x.get('created_utc', 0), reverse=True)
            
            logging.info(f"Retrieved {len(all_content)} total Reddit content items for user {username}")
            return all_content
            
        except Exception as e:
            logging.error(f"Error getting Reddit user content: {str(e)}")
            raise CustomException(f"Failed to get user content: {str(e)}", sys)
