"""
Stress analysis service that processes tweets and detects stress levels.
"""
import re
from typing import List, Dict, Optional
from datetime import datetime
from src.logger import logging
from src.exception import CustomException
from src.pipeline.predict_pipeline import PredictPipeline
import sys

class StressAnalyzer:
    """Service for analyzing stress levels in tweets"""
    
    # Stress indicators (keywords and patterns)
    STRESS_KEYWORDS = {
        'high': [
            'overwhelmed', 'exhausted', 'anxious', 'stressed', 'panic', 'worried',
            'frustrated', 'angry', 'depressed', 'hopeless', 'tired', 'burnout',
            'can\'t cope', 'breaking point', 'mental breakdown', 'too much',
            'drowning', 'suffocating', 'trapped', 'stuck', 'helpless'
        ],
        'moderate': [
            'busy', 'tired', 'stressed', 'worried', 'concerned', 'pressure',
            'deadline', 'overwhelming', 'difficult', 'challenging', 'struggling',
            'hard time', 'not easy', 'tough', 'rough day', 'long day'
        ],
        'low': [
            'relaxed', 'calm', 'peaceful', 'happy', 'content', 'grateful',
            'blessed', 'excited', 'motivated', 'energized', 'positive'
        ]
    }
    
    # Negative sentiment patterns
    NEGATIVE_PATTERNS = [
        r'\b(no|not|never|can\'t|won\'t|don\'t|isn\'t|aren\'t)\b',
        r'\b(why|how|what)\s+(is|are|was|were)\s+wrong',
        r'\b(feel|feeling)\s+(bad|terrible|awful|horrible)',
        r'\b(hate|dislike|annoyed|irritated)',
    ]
    
    def __init__(self):
        self.predict_pipeline = PredictPipeline()
        logging.info("StressAnalyzer initialized")
    
    def analyze_tweet(self, tweet_text: str) -> Dict:
        """
        Analyze a single tweet for stress indicators.
        
        Args:
            tweet_text: The text content of the tweet
            
        Returns:
            Dictionary with stress analysis results
        """
        try:
            if not tweet_text or not isinstance(tweet_text, str):
                return {
                    'stress_score': 0.0,
                    'has_stress_indicators': False,
                    'indicators_found': [],
                    'sentiment': 'neutral'
                }
            
            text_lower = tweet_text.lower()
            stress_score = 0.0
            indicators_found = []
            sentiment = 'neutral'
            
            # Check for high stress keywords
            high_stress_count = sum(1 for keyword in self.STRESS_KEYWORDS['high'] 
                                   if keyword in text_lower)
            if high_stress_count > 0:
                stress_score += 0.4 * min(high_stress_count, 3)  # Cap at 3 occurrences
                indicators_found.extend([kw for kw in self.STRESS_KEYWORDS['high'] 
                                       if kw in text_lower])
                sentiment = 'negative'
            
            # Check for moderate stress keywords
            moderate_stress_count = sum(1 for keyword in self.STRESS_KEYWORDS['moderate'] 
                                       if keyword in text_lower)
            if moderate_stress_count > 0:
                stress_score += 0.2 * min(moderate_stress_count, 2)
                indicators_found.extend([kw for kw in self.STRESS_KEYWORDS['moderate'] 
                                       if kw in text_lower])
                if sentiment == 'neutral':
                    sentiment = 'slightly_negative'
            
            # Check for negative patterns
            for pattern in self.NEGATIVE_PATTERNS:
                if re.search(pattern, text_lower):
                    stress_score += 0.1
                    indicators_found.append('negative_pattern')
                    if sentiment == 'neutral':
                        sentiment = 'slightly_negative'
            
            # Check for positive keywords (reduce stress score)
            positive_count = sum(1 for keyword in self.STRESS_KEYWORDS['low'] 
                               if keyword in text_lower)
            if positive_count > 0:
                stress_score -= 0.15 * min(positive_count, 2)
                if sentiment == 'neutral' or sentiment == 'slightly_negative':
                    sentiment = 'positive'
            
            # Normalize stress score (0.0 to 1.0)
            stress_score = max(0.0, min(1.0, stress_score))
            
            # Determine if tweet has stress indicators
            has_stress_indicators = stress_score > 0.3 or len(indicators_found) > 0
            
            return {
                'stress_score': round(stress_score, 3),
                'has_stress_indicators': has_stress_indicators,
                'indicators_found': list(set(indicators_found)),  # Remove duplicates
                'sentiment': sentiment,
                'tweet_text': tweet_text[:200]  # Store first 200 chars
            }
            
        except Exception as e:
            logging.error(f"Error analyzing tweet: {str(e)}")
            return {
                'stress_score': 0.0,
                'has_stress_indicators': False,
                'indicators_found': [],
                'sentiment': 'neutral',
                'error': str(e)
            }
    
    def analyze_tweets(self, tweets: List[Dict]) -> Dict:
        """
        Analyze multiple tweets and generate overall stress assessment.
        
        Args:
            tweets: List of tweet dictionaries with 'text' field
            
        Returns:
            Dictionary with comprehensive stress analysis
        """
        try:
            if not tweets:
                return {
                    'stress_level': 0.0,
                    'stress_category': 'low',
                    'confidence_score': 0.0,
                    'total_tweets_analyzed': 0,
                    'tweets_with_stress_indicators': 0,
                    'average_sentiment': 0.0,
                    'detailed_metrics': {},
                    'tweet_samples': []
                }
            
            start_time = datetime.utcnow()
            tweet_analyses = []
            total_stress_score = 0.0
            tweets_with_stress = 0
            sentiment_scores = []
            
            # Analyze each tweet
            for tweet in tweets:
                tweet_text = tweet.get('text', '')
                if not tweet_text:
                    continue
                
                analysis = self.analyze_tweet(tweet_text)
                tweet_analyses.append({
                    'tweet_id': tweet.get('id'),
                    'created_at': tweet.get('created_at'),
                    'analysis': analysis
                })
                
                total_stress_score += analysis['stress_score']
                if analysis['has_stress_indicators']:
                    tweets_with_stress += 1
                
                # Convert sentiment to numeric score
                sentiment_map = {
                    'positive': 1.0,
                    'neutral': 0.5,
                    'slightly_negative': 0.3,
                    'negative': 0.0
                }
                sentiment_scores.append(sentiment_map.get(analysis['sentiment'], 0.5))
            
            # Calculate overall metrics
            total_tweets = len(tweet_analyses)
            if total_tweets == 0:
                return {
                    'stress_level': 0.0,
                    'stress_category': 'low',
                    'confidence_score': 0.0,
                    'total_tweets_analyzed': 0,
                    'tweets_with_stress_indicators': 0,
                    'average_sentiment': 0.0,
                    'detailed_metrics': {},
                    'tweet_samples': []
                }
            
            average_stress = total_stress_score / total_tweets
            average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5
            stress_percentage = (tweets_with_stress / total_tweets) * 100
            
            # Determine stress category
            if average_stress >= 0.7:
                stress_category = 'very_high'
            elif average_stress >= 0.5:
                stress_category = 'high'
            elif average_stress >= 0.3:
                stress_category = 'moderate'
            else:
                stress_category = 'low'
            
            # Calculate confidence score
            # Higher confidence with more tweets and consistent patterns
            confidence_score = min(0.95, 0.5 + (total_tweets / 200) * 0.3)
            if tweets_with_stress > 0:
                consistency = min(1.0, stress_percentage / 50)
                confidence_score += consistency * 0.15
            
            # Get sample tweets with highest stress
            high_stress_tweets = sorted(
                tweet_analyses,
                key=lambda x: x['analysis']['stress_score'],
                reverse=True
            )[:5]
            
            tweet_samples = [
                {
                    'tweet_id': t['tweet_id'],
                    'text': t['analysis']['tweet_text'],
                    'stress_score': t['analysis']['stress_score'],
                    'indicators': t['analysis']['indicators_found'],
                    'created_at': t.get('created_at')
                }
                for t in high_stress_tweets
            ]
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            result = {
                'stress_level': round(average_stress, 3),
                'stress_category': stress_category,
                'confidence_score': round(confidence_score, 3),
                'total_tweets_analyzed': total_tweets,
                'tweets_with_stress_indicators': tweets_with_stress,
                'stress_percentage': round(stress_percentage, 2),
                'average_sentiment': round(average_sentiment, 3),
                'detailed_metrics': {
                    'total_stress_score': round(total_stress_score, 3),
                    'average_stress_per_tweet': round(average_stress, 3),
                    'sentiment_distribution': {
                        'positive': sum(1 for a in tweet_analyses if a['analysis']['sentiment'] == 'positive'),
                        'neutral': sum(1 for a in tweet_analyses if a['analysis']['sentiment'] == 'neutral'),
                        'negative': sum(1 for a in tweet_analyses if a['analysis']['sentiment'] in ['slightly_negative', 'negative'])
                    }
                },
                'tweet_samples': tweet_samples,
                'processing_time_seconds': round(processing_time, 3)
            }
            
            logging.info(f"Analyzed {total_tweets} tweets. Stress level: {stress_category} ({average_stress:.3f})")
            return result
            
        except Exception as e:
            logging.error(f"Error analyzing tweets: {str(e)}")
            raise CustomException(f"Failed to analyze tweets: {str(e)}", sys)
    
    def analyze_user_tweets(self, tweets: List[Dict], username: str) -> Dict:
        """
        Analyze user tweets and return formatted results.
        
        Args:
            tweets: List of tweet dictionaries
            username: Username being analyzed
            
        Returns:
            Dictionary with analysis results ready for database storage
        """
        try:
            analysis_result = self.analyze_tweets(tweets)
            
            return {
                'username_analyzed': username,
                'stress_level': analysis_result['stress_level'],
                'stress_category': analysis_result['stress_category'],
                'confidence_score': analysis_result['confidence_score'],
                'total_tweets_analyzed': analysis_result['total_tweets_analyzed'],
                'tweets_with_stress_indicators': analysis_result['tweets_with_stress_indicators'],
                'average_sentiment': analysis_result['average_sentiment'],
                'detailed_metrics': analysis_result['detailed_metrics'],
                'tweet_samples': analysis_result['tweet_samples'],
                'processing_time_seconds': analysis_result.get('processing_time_seconds', 0)
            }
            
        except Exception as e:
            logging.error(f"Error in analyze_user_tweets: {str(e)}")
            raise CustomException(f"Failed to analyze user tweets: {str(e)}", sys)
