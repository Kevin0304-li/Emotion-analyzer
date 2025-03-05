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

class VaderSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.response_generator = ResponseGenerator()
        
        # Punctuation patterns and their emotional impact
        self.punctuation_patterns = {
            # Question marks - indicate curiosity, uncertainty, or intensity
            r'\?+': {
                'single': {'emotion': 'curious', 'intensity': 1.2},
                'multiple': {'emotion': 'confused', 'intensity': 1.5}
            },
            # Exclamation marks - indicate strong emotions
            r'!+': {
                'single': {'emotion': 'excited', 'intensity': 1.3},
                'multiple': {'emotion': 'ecstatic', 'intensity': 1.8}
            },
            # Combined question and exclamation - indicate strong surprise or confusion
            r'[?!]+': {
                'single': {'emotion': 'surprised', 'intensity': 1.4},
                'multiple': {'emotion': 'shocked', 'intensity': 1.9}
            },
            # Ellipsis - indicate uncertainty or trailing thoughts
            r'\.{3,}': {
                'single': {'emotion': 'thoughtful', 'intensity': 1.1},
                'multiple': {'emotion': 'contemplative', 'intensity': 1.3}
            },
            # Period - neutral or calm
            r'\.': {
                'single': {'emotion': 'calm', 'intensity': 1.0}
            }
        }
        
        # Enhanced emotion categories with more nuanced emotions
        self.emotions = {
            'positive': {
                'ecstatic': {'compound': 0.9, 'pos': 0.8, 'neg': 0.1},
                'excited': {'compound': 0.8, 'pos': 0.7, 'neg': 0.1},
                'happy': {'compound': 0.7, 'pos': 0.6, 'neg': 0.1},
                'pleased': {'compound': 0.6, 'pos': 0.5, 'neg': 0.1},
                'grateful': {'compound': 0.7, 'pos': 0.6, 'neg': 0.1},
                'proud': {'compound': 0.7, 'pos': 0.6, 'neg': 0.1},
                'optimistic': {'compound': 0.6, 'pos': 0.5, 'neg': 0.1},
                'inspired': {'compound': 0.7, 'pos': 0.6, 'neg': 0.1},
                'confident': {'compound': 0.6, 'pos': 0.5, 'neg': 0.1},
                'peaceful': {'compound': 0.5, 'pos': 0.4, 'neg': 0.1}
            },
            'negative': {
                'furious': {'compound': -0.9, 'pos': 0.1, 'neg': 0.8},
                'angry': {'compound': -0.8, 'pos': 0.1, 'neg': 0.7},
                'frustrated': {'compound': -0.7, 'pos': 0.1, 'neg': 0.6},
                'annoyed': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5},
                'anxious': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5},
                'worried': {'compound': -0.5, 'pos': 0.1, 'neg': 0.4},
                'overwhelmed': {'compound': -0.7, 'pos': 0.1, 'neg': 0.6},
                'stressed': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5},
                'irritated': {'compound': -0.5, 'pos': 0.1, 'neg': 0.4},
                'disappointed': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5}
            },
            'sad': {
                'devastated': {'compound': -0.9, 'pos': 0.1, 'neg': 0.8},
                'heartbroken': {'compound': -0.8, 'pos': 0.1, 'neg': 0.7},
                'sad': {'compound': -0.7, 'pos': 0.1, 'neg': 0.6},
                'disappointed': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5},
                'down': {'compound': -0.5, 'pos': 0.1, 'neg': 0.4},
                'lonely': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5},
                'grief': {'compound': -0.8, 'pos': 0.1, 'neg': 0.7},
                'melancholic': {'compound': -0.7, 'pos': 0.1, 'neg': 0.6},
                'nostalgic': {'compound': -0.5, 'pos': 0.2, 'neg': 0.4},
                'homesick': {'compound': -0.6, 'pos': 0.1, 'neg': 0.5}
            },
            'complex': {
                'confused': {'compound': 0.0, 'pos': 0.3, 'neg': 0.3},
                'surprised': {'compound': 0.5, 'pos': 0.4, 'neg': 0.2},
                'shocked': {'compound': 0.0, 'pos': 0.3, 'neg': 0.3},
                'amazed': {'compound': 0.7, 'pos': 0.6, 'neg': 0.1},
                'puzzled': {'compound': -0.2, 'pos': 0.2, 'neg': 0.3},
                'curious': {'compound': 0.3, 'pos': 0.3, 'neg': 0.1},
                'thoughtful': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'contemplative': {'compound': 0.1, 'pos': 0.2, 'neg': 0.1},
                'reflective': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'nostalgic': {'compound': -0.3, 'pos': 0.2, 'neg': 0.3}
            },
            'neutral': {
                'calm': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'thoughtful': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'curious': {'compound': 0.3, 'pos': 0.3, 'neg': 0.1},
                'focused': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'determined': {'compound': 0.3, 'pos': 0.3, 'neg': 0.1},
                'mindful': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'attentive': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'observant': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'patient': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1},
                'balanced': {'compound': 0.2, 'pos': 0.2, 'neg': 0.1}
            }
        }
        
        # Emotion intensity modifiers
        self.intensity_modifiers = {
            'very': 1.5,
            'really': 1.5,
            'extremely': 2.0,
            'absolutely': 2.0,
            'slightly': 0.7,
            'a bit': 0.7,
            'kind of': 0.7,
            'sort of': 0.7
        }
        
        # Context-based emotion adjustments
        self.context_patterns = {
            'grief': r'(death|loss|passed away|died|mourning)',
            'anxiety': r'(worry|anxious|panic|stress|pressure)',
            'excitement': r'(amazing|incredible|wonderful|fantastic)',
            'frustration': r'(annoying|frustrating|difficult|hard|trouble)',
            'gratitude': r'(thank|grateful|appreciate|blessed)',
            'pride': r'(proud|accomplish|achievement|success)',
            'nostalgia': r'(remember|memory|childhood|past)',
            'hope': r'(hope|wish|dream|future|tomorrow)',
            'disappointment': r'(let down|disappoint|fail|mistake)',
            'surprise': r'(surprise|shock|unexpected|suddenly)'
        }

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using VADER."""
        return self.sia.polarity_scores(text)

    def _get_intensity_modifier(self, text: str) -> float:
        """Calculate intensity modifier based on text."""
        modifier = 1.0
        for word, value in self.intensity_modifiers.items():
            if word in text.lower():
                modifier *= value
        return modifier

    def _get_context_adjustment(self, text: str) -> Tuple[str, float]:
        """Get context-based emotion adjustment."""
        for emotion, pattern in self.context_patterns.items():
            if re.search(pattern, text.lower()):
                return emotion, 1.5
        return '', 1.0

    def _analyze_punctuation(self, text: str) -> Tuple[str, float]:
        """Analyze punctuation patterns and their emotional impact."""
        max_intensity = 1.0
        dominant_emotion = None
        
        for pattern, impacts in self.punctuation_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                punctuation = match.group()
                if len(punctuation) > 1:
                    impact = impacts.get('multiple', impacts['single'])
                else:
                    impact = impacts['single']
                
                if impact['intensity'] > max_intensity:
                    max_intensity = impact['intensity']
                    dominant_emotion = impact['emotion']
        
        return dominant_emotion, max_intensity

    def determine_emotion(self, text: str) -> str:
        """Determine emotion based on sentiment analysis, context, and punctuation."""
        # Get base sentiment scores
        sentiment = self.analyze_sentiment(text)
        
        # Apply intensity modifier
        intensity_modifier = self._get_intensity_modifier(text)
        sentiment['compound'] *= intensity_modifier
        
        # Get context adjustment
        context_emotion, context_multiplier = self._get_context_adjustment(text)
        
        # Analyze punctuation
        punctuation_emotion, punctuation_intensity = self._analyze_punctuation(text)
        
        # Determine base emotion category
        if sentiment['compound'] >= 0.5:
            category = 'positive'
            emotions = self.emotions['positive']
        elif sentiment['compound'] <= -0.5:
            if context_emotion in ['grief', 'heartbroken']:
                category = 'sad'
                emotions = self.emotions['sad']
            else:
                category = 'negative'
                emotions = self.emotions['negative']
        else:
            if context_emotion in ['confused', 'surprised', 'shocked', 'puzzled']:
                category = 'complex'
                emotions = self.emotions['complex']
            else:
                category = 'neutral'
                emotions = self.emotions['neutral']
        
        # Find the closest matching emotion
        closest_emotion = None
        min_diff = float('inf')
        
        for emotion, thresholds in emotions.items():
            diff = abs(sentiment['compound'] - thresholds['compound'])
            if diff < min_diff:
                min_diff = diff
                closest_emotion = emotion
        
        # Adjust emotion based on punctuation if it has a stronger impact
        if punctuation_emotion and punctuation_intensity > 1.2:
            closest_emotion = punctuation_emotion
        
        return closest_emotion

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
        # Initialize sentiment analyzer
        analyzer = VaderSentimentAnalyzer()
        logging.info("VADER Sentiment Analysis Chatbot starting...")
        
        print("\nWelcome to the Emotion Analyzer Chatbot!")
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
                
                # Analyze sentiment and determine emotion
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
