import os

# Create directories if they don't exist
os.makedirs('responses', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Write app.py
app_content = '''# -*- coding: utf-8 -*-
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
'''

# Write response_generator.py
response_generator_content = '''# -*- coding: utf-8 -*-
from typing import Dict, Optional
import random

class ResponseGenerator:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        
    def generate_response(self, 
                         user_input: str,
                         emotion: str,
                         context: Optional[Dict] = None) -> str:
        """
        Generate a response based on user input and emotion
        """
        # Base responses based on emotion
        responses = {
            'happy': [
                "That's wonderful!",
                "I'm glad to hear that!",
                "That makes me happy too!",
                "How exciting!"
            ],
            'excited': [
                "That's amazing!",
                "I'm thrilled to hear that!",
                "This is fantastic!",
                "How wonderful!"
            ],
            'ecstatic': [
                "This is absolutely incredible!",
                "I'm overjoyed!",
                "This is the best thing ever!",
                "I'm so excited I can't contain myself!"
            ],
            'sad': [
                "I'm sorry to hear that.",
                "That must be difficult.",
                "I understand how you feel.",
                "Let me know if you want to talk about it."
            ],
            'frustrated': [
                "I understand your frustration.",
                "That sounds frustrating.",
                "I can see why you'd feel that way.",
                "Let's work through this together."
            ],
            'angry': [
                "I can see why you're angry.",
                "That's completely understandable.",
                "I understand your anger.",
                "Let's take a moment to process this."
            ],
            'furious': [
                "I can feel your anger.",
                "That's absolutely infuriating.",
                "I understand your intense frustration.",
                "This is completely unacceptable."
            ],
            'neutral': [
                "I understand.",
                "I see.",
                "Interesting.",
                "Tell me more."
            ],
            'calm': [
                "I feel at peace with that.",
                "That's quite calming.",
                "I understand your perspective.",
                "Let's maintain this peaceful state."
            ],
            'thoughtful': [
                "That's an interesting perspective.",
                "Let me think about that.",
                "I'll consider that carefully.",
                "That's worth reflecting on."
            ],
            'curious': [
                "That's fascinating!",
                "I'd love to learn more about that.",
                "Could you tell me more?",
                "That's very interesting."
            ]
        }
        
        # Get base response
        if emotion in responses:
            base_response = random.choice(responses[emotion])
        else:
            base_response = random.choice(responses['neutral'])
            
        return base_response
'''

# Write the files with proper encoding
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

with open('responses/response_generator.py', 'w', encoding='utf-8') as f:
    f.write(response_generator_content)

print("Files created successfully!") 