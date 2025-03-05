# -*- coding: utf-8 -*-
import os
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from responses.response_generator import ResponseGenerator

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VaderSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
        # Define emotion categories and their thresholds
        self.emotion_categories = {
            # Positive emotions
            'ecstatic': {'threshold': 0.8, 'sentiment': 'positive'},
            'excited': {'threshold': 0.6, 'sentiment': 'positive'},
            'happy': {'threshold': 0.4, 'sentiment': 'positive'},
            'pleased': {'threshold': 0.2, 'sentiment': 'positive'},
            
            # Negative emotions
            'furious': {'threshold': -0.8, 'sentiment': 'negative'},
            'angry': {'threshold': -0.6, 'sentiment': 'negative'},
            'frustrated': {'threshold': -0.4, 'sentiment': 'negative'},
            'annoyed': {'threshold': -0.2, 'sentiment': 'negative'},
            
            # Sad emotions
            'devastated': {'threshold': -0.8, 'sentiment': 'negative', 'type': 'sad'},
            'sad': {'threshold': -0.6, 'sentiment': 'negative', 'type': 'sad'},
            'disappointed': {'threshold': -0.4, 'sentiment': 'negative', 'type': 'sad'},
            'down': {'threshold': -0.2, 'sentiment': 'negative', 'type': 'sad'},
            
            # Neutral emotions
            'neutral': {'threshold': 0.0, 'sentiment': 'neutral'},
            'calm': {'threshold': 0.0, 'sentiment': 'neutral', 'type': 'calm'},
            'thoughtful': {'threshold': 0.0, 'sentiment': 'neutral', 'type': 'thoughtful'},
            'curious': {'threshold': 0.0, 'sentiment': 'neutral', 'type': 'curious'}
        }
        
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment using VADER with enhanced emotion detection
        """
        # Get sentiment scores
        scores = self.sia.polarity_scores(text)
        compound_score = scores['compound']
        
        # Determine base sentiment
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        # Determine emotion based on compound score and context
        emotion = self._determine_emotion(compound_score, text)
            
        return {
            'sentiment': sentiment,
            'emotion': emotion,
            'scores': scores,
            'text': text
        }
        
    def _determine_emotion(self, compound_score: float, text: str) -> str:
        """
        Determine the most appropriate emotion based on score and context
        """
        # Convert text to lowercase for word matching
        text_lower = text.lower()
        
        # Check for specific emotion indicators in text
        if any(word in text_lower for word in ['love', 'amazing', 'wonderful', 'fantastic']):
            return 'ecstatic'
        elif any(word in text_lower for word in ['hate', 'terrible', 'awful', 'horrible']):
            return 'furious'
        elif any(word in text_lower for word in ['sad', 'unhappy', 'miserable', 'depressed']):
            return 'devastated'
        elif any(word in text_lower for word in ['calm', 'peaceful', 'relaxed', 'serene']):
            return 'calm'
        elif any(word in text_lower for word in ['think', 'wonder', 'consider', 'reflect']):
            return 'thoughtful'
        elif any(word in text_lower for word in ['why', 'how', 'what', 'when', 'where']):
            return 'curious'
            
        # If no specific indicators, use score-based emotion
        for emotion, criteria in self.emotion_categories.items():
            if criteria['sentiment'] == 'positive' and compound_score >= criteria['threshold']:
                return emotion
            elif criteria['sentiment'] == 'negative' and compound_score <= criteria['threshold']:
                return emotion
            elif criteria['sentiment'] == 'neutral' and abs(compound_score) < 0.05:
                return emotion
                
        # Default to neutral if no other emotion matches
        return 'neutral'

def main():
    try:
        # Initialize components
        sentiment_analyzer = VaderSentimentAnalyzer()
        response_generator = ResponseGenerator(None)
        
        logger.info("Starting VADER Sentiment Analysis Chatbot")
        print("VADER Sentiment Analysis Chatbot (type 'exit' to quit)")
        
        while True:
            try:
                # Get user input
                user_input = input("> ").strip()
                if not user_input:
                    continue
                    
                if user_input.lower() == 'exit':
                    logger.info("User requested to exit")
                    break
                    
                # Analyze sentiment
                analysis_result = sentiment_analyzer.analyze(user_input)
                
                # Get emotion and generate response
                emotion = analysis_result['emotion']
                response = response_generator.generate_response(
                    user_input=user_input,
                    emotion=emotion,
                    context=None
                )
                
                # Display response with emotion
                print(f"[{emotion}] {response}")
                
            except Exception as e:
                logger.error(f"Error processing user input: {str(e)}")
                print("I apologize, but I encountered an error. Please try again.")
                
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print("A fatal error occurred. Please check your configuration and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
