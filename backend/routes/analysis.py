"""
Analysis routes for stress detection (Twitter and Reddit).
"""
from flask import Blueprint, request, jsonify, session
from backend.models import db, User, Analysis
from backend.services.twitter_api import TwitterAPIService
from backend.services.reddit_api import RedditAPIService
from backend.services.stress_analyzer import StressAnalyzer
from backend.config import Config
from src.logger import logging
from src.exception import CustomException
import sys

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_user():
    """Analyze user content (Twitter or Reddit) for stress levels"""
    try:
        # Check authentication
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'Authentication required'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        username = data.get('username', '').strip()
        platform = data.get('platform', 'twitter').lower()  # 'twitter' or 'reddit'
        
        # Validate platform
        if platform not in ['twitter', 'reddit']:
            return jsonify({
                'status': 'error',
                'message': 'Platform must be "twitter" or "reddit"'
            }), 400
        
        # Clean username based on platform
        if platform == 'twitter':
            username = username.lstrip('@')
        elif platform == 'reddit':
            username = username.replace('u/', '').replace('/u/', '').strip()
        
        # Use authenticated user's username if not provided
        if not username:
            username = user.username
        
        # Determine analysis type
        if platform == 'twitter':
            analysis_type = 'oauth' if user.is_twitter_connected else 'manual'
        else:  # reddit
            analysis_type = 'oauth' if user.is_reddit_connected else 'manual'
        
        # Initialize analyzer
        analyzer = StressAnalyzer()
        content_items = []
        analysis_result = None
        
        # Fetch and analyze based on platform
        if platform == 'twitter':
            # Twitter analysis
            twitter_service = TwitterAPIService()
            
            # If user has OAuth, use their access token
            if user.is_twitter_connected and user.twitter_access_token:
                twitter_service.set_access_token(user.twitter_access_token)
            # Otherwise, use bearer token if available
            elif Config.TWITTER_API_BEARER_TOKEN:
                twitter_service = TwitterAPIService(Config.TWITTER_API_BEARER_TOKEN)
            
            # Get user info
            try:
                user_info = twitter_service.get_user_by_username(username)
                twitter_user_id = user_info.get('id')
            except CustomException as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Could not find Twitter user @{username}. Please check the username and try again.'
                }), 404
            
            # Get tweets
            try:
                tweets = twitter_service.get_user_tweets(
                    twitter_user_id,
                    max_results=Config.MAX_TWEETS_TO_ANALYZE,
                )
            except CustomException as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to fetch tweets: {str(e)}'
                }), 500
            
            if not tweets:
                return jsonify({
                    'status': 'error',
                    'message': f'No tweets found for @{username} in the last {Config.TWEET_LOOKBACK_DAYS} days'
                }), 404
            
            # Analyze tweets
            analysis_result = analyzer.analyze_user_tweets(tweets, username)
            content_items = tweets
            
        else:  # platform == 'reddit'
            # Reddit analysis
            reddit_service = RedditAPIService(user_agent=Config.REDDIT_USER_AGENT)
            
            # If user has OAuth, use their access token
            if user.is_reddit_connected and user.reddit_access_token:
                reddit_service.set_access_token(user.reddit_access_token)
            
            # Get user info
            try:
                user_info = reddit_service.get_user_by_username(username)
            except CustomException as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Could not find Reddit user u/{username}. Please check the username and try again.'
                }), 404
            
            # Get posts and comments
            try:
                content_items = reddit_service.get_user_content(
                    username,
                    include_comments=True,
                    max_posts=Config.MAX_REDDIT_POSTS_TO_ANALYZE,
                    max_comments=Config.MAX_REDDIT_COMMENTS_TO_ANALYZE
                )
            except CustomException as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to fetch Reddit content: {str(e)}'
                }), 500
            
            if not content_items:
                return jsonify({
                    'status': 'error',
                    'message': f'No posts or comments found for u/{username}'
                }), 404
            
            # Analyze Reddit content (posts and comments)
            # Convert Reddit format to analysis format
            reddit_content = []
            for item in content_items:
                text = item.get('text') or item.get('selftext') or item.get('title', '')
                if text:
                    reddit_content.append({
                        'id': item.get('id'),
                        'text': text,
                        'created_at': item.get('created_at'),
                        'content_type': item.get('content_type', 'post')
                    })
            
            analysis_result = analyzer.analyze_tweets(reddit_content)  # Reuse same analyzer
            analysis_result['username_analyzed'] = username
        
        # Save analysis to database
        analysis = Analysis(
            user_id=user.id,
            platform=platform,
            analysis_type=analysis_type,
            username_analyzed=username,
            stress_level=analysis_result['stress_level'],
            stress_category=analysis_result['stress_category'],
            confidence_score=analysis_result['confidence_score'],
            total_posts_analyzed=analysis_result['total_tweets_analyzed'],
            posts_with_stress_indicators=analysis_result['tweets_with_stress_indicators'],
            average_sentiment=analysis_result['average_sentiment'],
            detailed_metrics=analysis_result['detailed_metrics'],
            content_samples=analysis_result['tweet_samples'],
            processing_time_seconds=analysis_result['processing_time_seconds']
        )
        
        db.session.add(analysis)
        user.last_analysis_at = analysis.analysis_date
        db.session.commit()
        
        platform_prefix = '@' if platform == 'twitter' else 'u/'
        logging.info(f"Analysis completed for {platform_prefix}{username} ({platform}): {analysis_result['stress_category']}")
        
        return jsonify({
            'status': 'success',
            'platform': platform,
            'analysis': analysis.to_dict()
        }), 200
        
    except CustomException as e:
        logging.error(f"Custom exception in analyze: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        logging.error(f"Error in analyze: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'An error occurred during analysis: {str(e)}'
        }), 500

@analysis_bp.route('/history', methods=['GET'])
def get_analysis_history():
    """Get user's analysis history"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'Authentication required'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        # Get recent analyses
        analyses = Analysis.query.filter_by(user_id=user.id)\
            .order_by(Analysis.analysis_date.desc())\
            .limit(10)\
            .all()
        
        return jsonify({
            'status': 'success',
            'analyses': [analysis.to_dict() for analysis in analyses]
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting analysis history: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@analysis_bp.route('/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get specific analysis by ID"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'Authentication required'
            }), 401
        
        analysis = Analysis.query.get(analysis_id)
        if not analysis:
            return jsonify({
                'status': 'error',
                'message': 'Analysis not found'
            }), 404
        
        # Verify ownership
        if analysis.user_id != user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 403
        
        return jsonify({
            'status': 'success',
            'analysis': analysis.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Error getting analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
