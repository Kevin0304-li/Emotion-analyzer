# -*- coding: utf-8 -*-
import os
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, Tuple, Optional
import re
from responses.response_generator import ResponseGenerator

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)

class EmotionAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.response_generator = ResponseGenerator()
        
        # Initialize patterns
        self._initialize_patterns()
        
    def _initialize_patterns(self):
        """Initialize patterns for rule-based analysis."""
        self.greeting_patterns = {
            'neutral': re.compile(r'^(hi|hello|hey)$', re.IGNORECASE),
            'excited': re.compile(r'^(hi+|hello+|hey+)!*$', re.IGNORECASE)
        }
        
        self.question_patterns = {
            'curious': re.compile(r'^(why|what|how|when|where|who)\??$', re.IGNORECASE),
            'confused': re.compile(r'\?{2,}'),
            'rhetorical': re.compile(r'(really\?|seriously\?|right\?)', re.IGNORECASE)
        }
        
        self.strong_emotion_patterns = {
            'angry': re.compile(r'\b(hate|angry|mad|furious)\b', re.IGNORECASE),
            'happy': re.compile(r'\b(love|happy|joy|wonderful)\b', re.IGNORECASE),
            'sad': re.compile(r'\b(sad|depressed|miserable)\b', re.IGNORECASE)
        }

    def determine_emotion(self, text: str) -> str:
        """Determine emotion using pattern matching and VADER."""
        # Check greetings
        for emotion, pattern in self.greeting_patterns.items():
            if pattern.match(text):
                return emotion
                
        # Check questions
        for emotion, pattern in self.question_patterns.items():
            if pattern.search(text):
                return emotion
                
        # Check strong emotions
        for emotion, pattern in self.strong_emotion_patterns.items():
            if pattern.search(text):
                return emotion
        
        # Use VADER for general sentiment
        sentiment = self.sia.polarity_scores(text)
        
        # Map sentiment to emotions
        if sentiment['compound'] >= 0.5:
            return 'happy'
        elif sentiment['compound'] <= -0.5:
            return 'sad'
        elif -0.1 <= sentiment['compound'] <= 0.1:
            return 'neutral'
        elif sentiment['compound'] > 0.1:
            return 'positive'
        else:
            return 'negative'

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('emotion_analyzer.log'),
            logging.StreamHandler()
        ]
    )
    
    try:
        # Initialize analyzer
        analyzer = EmotionAnalyzer()
        logging.info("Emotion Analyzer starting...")
        
        print("\nWelcome to the Emotion Analyzer!")
        print("Type your message and I'll analyze your emotions.")
        print("Type 'exit' to quit.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("> ").strip()
                
                if user_input.lower() == 'exit':
                    print("\nGoodbye! Have a great day!")
                    break
                
                if not user_input:
                    continue
                
                # Analyze emotion
                emotion = analyzer.determine_emotion(user_input)
                
                # Generate response
                response = analyzer.response_generator.generate_response(emotion, user_input)
                
                # Print response with emotion tag
                print(f"[{emotion}] {response}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye! Have a great day!")
                break
            except Exception as e:
                logging.error(f"Error processing input: {str(e)}")
                print("I'm having trouble understanding that. Could you rephrase it?")
                
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        print("An error occurred. Please try again later.")

if __name__ == "__main__":
    main()
