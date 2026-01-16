"""
Configuration settings for the backend application.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///detect_stress.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Twitter/X OAuth Configuration
    TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID', '')
    TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET', '')
    TWITTER_REDIRECT_URI = os.getenv('TWITTER_REDIRECT_URI', 'http://localhost:5173/auth/callback')
    TWITTER_API_BEARER_TOKEN = os.getenv('TWITTER_API_BEARER_TOKEN', '')
    
    # Twitter API v2 Configuration
    TWITTER_API_BASE_URL = 'https://api.twitter.com/2'
    TWITTER_OAUTH_BASE_URL = 'https://twitter.com/i/oauth2'
    
    # Reddit OAuth Configuration
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI', 'http://localhost:5173/auth/reddit/callback')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'DetectTheStress/1.0 by YourUsername')
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    
    # Analysis Configuration
    MAX_TWEETS_TO_ANALYZE = int(os.getenv('MAX_TWEETS_TO_ANALYZE', '100'))
    TWEET_LOOKBACK_DAYS = int(os.getenv('TWEET_LOOKBACK_DAYS', '30'))
    MAX_REDDIT_POSTS_TO_ANALYZE = int(os.getenv('MAX_REDDIT_POSTS_TO_ANALYZE', '100'))
    MAX_REDDIT_COMMENTS_TO_ANALYZE = int(os.getenv('MAX_REDDIT_COMMENTS_TO_ANALYZE', '50'))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_detect_stress.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
