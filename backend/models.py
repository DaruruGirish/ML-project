"""
Database models for the Detect The Stress application.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, index=True)
    display_name = Column(String(100), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    
    # Twitter fields
    twitter_id = Column(String(50), unique=True, nullable=True, index=True)
    twitter_access_token = Column(Text, nullable=True)  # Encrypted in production
    twitter_refresh_token = Column(Text, nullable=True)  # Encrypted in production
    is_twitter_connected = Column(Boolean, default=False)
    
    # Reddit fields
    reddit_id = Column(String(50), unique=True, nullable=True, index=True)
    reddit_access_token = Column(Text, nullable=True)  # Encrypted in production
    reddit_refresh_token = Column(Text, nullable=True)  # Encrypted in production
    is_reddit_connected = Column(Boolean, default=False)
    reddit_karma = Column(Integer, default=0)
    
    # Legacy field for backward compatibility
    access_token = Column(Text, nullable=True)  # Deprecated - use platform-specific tokens
    refresh_token = Column(Text, nullable=True)  # Deprecated
    is_oauth_connected = Column(Boolean, default=False)  # Deprecated - use platform-specific flags
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analysis_at = Column(DateTime, nullable=True)
    
    # Relationships
    analyses = relationship('Analysis', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'profile_image_url': self.profile_image_url,
            'is_twitter_connected': self.is_twitter_connected,
            'is_reddit_connected': self.is_reddit_connected,
            'is_oauth_connected': self.is_oauth_connected or self.is_twitter_connected or self.is_reddit_connected,  # Backward compatibility
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_analysis_at': self.last_analysis_at.isoformat() if self.last_analysis_at else None,
        }
        if include_sensitive:
            data['twitter_id'] = self.twitter_id
            data['reddit_id'] = self.reddit_id
        return data

class Analysis(db.Model):
    """Analysis model for storing stress analysis results"""
    __tablename__ = 'analyses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    platform = Column(String(20), nullable=False, default='twitter')  # 'twitter' or 'reddit'
    analysis_type = Column(String(20), nullable=False)  # 'oauth' or 'manual'
    username_analyzed = Column(String(50), nullable=False)
    
    # Analysis Results
    stress_level = Column(Float, nullable=False)  # 0.0 to 1.0
    stress_category = Column(String(20), nullable=False)  # 'low', 'moderate', 'high', 'very_high'
    confidence_score = Column(Float, nullable=False)
    
    # Content Statistics (works for both Twitter and Reddit)
    total_posts_analyzed = Column(Integer, default=0)  # Renamed from total_tweets_analyzed
    posts_with_stress_indicators = Column(Integer, default=0)  # Renamed from tweets_with_stress_indicators
    average_sentiment = Column(Float, nullable=True)
    
    # Legacy fields for backward compatibility
    total_tweets_analyzed = Column(Integer, default=0)  # Deprecated - use total_posts_analyzed
    tweets_with_stress_indicators = Column(Integer, default=0)  # Deprecated - use posts_with_stress_indicators
    
    # Detailed Results (JSON)
    detailed_metrics = Column(JSON, nullable=True)  # Store detailed analysis
    content_samples = Column(JSON, nullable=True)  # Store sample posts with stress indicators (renamed from tweet_samples)
    tweet_samples = Column(JSON, nullable=True)  # Deprecated - use content_samples
    
    # Metadata
    analysis_date = Column(DateTime, default=datetime.utcnow, index=True)
    processing_time_seconds = Column(Float, nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='analyses')
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        # Use new field names, fall back to legacy for backward compatibility
        total_posts = self.total_posts_analyzed or self.total_tweets_analyzed or 0
        posts_with_stress = self.posts_with_stress_indicators or self.tweets_with_stress_indicators or 0
        samples = self.content_samples or self.tweet_samples
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'platform': self.platform,
            'analysis_type': self.analysis_type,
            'username_analyzed': self.username_analyzed,
            'stress_level': self.stress_level,
            'stress_category': self.stress_category,
            'confidence_score': self.confidence_score,
            'total_posts_analyzed': total_posts,
            'total_tweets_analyzed': total_posts,  # Backward compatibility
            'posts_with_stress_indicators': posts_with_stress,
            'tweets_with_stress_indicators': posts_with_stress,  # Backward compatibility
            'average_sentiment': self.average_sentiment,
            'detailed_metrics': self.detailed_metrics,
            'content_samples': samples,
            'tweet_samples': samples,  # Backward compatibility
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'processing_time_seconds': self.processing_time_seconds,
        }

class Resource(db.Model):
    """Resource model for storing mental health resources"""
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False)  # 'blog', 'wikipedia', 'game', 'meditation', etc.
    category = Column(String(50), nullable=True)  # 'audio', 'writing', 'practice', 'support', etc.
    url = Column(String(500), nullable=False)
    source = Column(String(100), nullable=True)
    icon_name = Column(String(50), nullable=True)  # For lucide-react icon names
    image_url = Column(String(500), nullable=True)  # URL for blog/article images
    read_time_minutes = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert resource to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'category': self.category,
            'url': self.url,
            'source': self.source,
            'icon_name': self.icon_name,
            'image_url': self.image_url,
            'read_time_minutes': self.read_time_minutes,
            'tags': self.tags or [],
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
