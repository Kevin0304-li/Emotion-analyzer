from transformers import pipeline
import numpy as np
from typing import Dict, List, Tuple

class SemanticAnalyzer:
    def __init__(self):
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
        
        # Initialize zero-shot classification for emotion detection
        self.emotion_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Define emotion categories
        self.emotion_categories = [
            "joy", "sadness", "anger", "fear", "surprise", "disgust",
            "trust", "anticipation", "neutral", "confusion"
        ]
        
        # Define semantic features to extract
        self.semantic_features = [
            "intensity", "formality", "certainty", "urgency",
            "sarcasm", "irony", "ambiguity"
        ]
        
    def analyze(self, text: str) -> Dict:
        """
        Perform deep semantic analysis of the text
        """
        # Get sentiment scores
        sentiment_scores = self.sentiment_analyzer(text)[0]
        
        # Get emotion probabilities
        emotion_results = self.emotion_classifier(
            text,
            candidate_labels=self.emotion_categories,
            multi_label=True
        )
        
        # Extract semantic features
        semantic_features = self._extract_semantic_features(text)
        
        # Combine all features into a rich representation
        emotional_representation = {
            'sentiment': {
                score['label']: score['score'] 
                for score in sentiment_scores
            },
            'emotions': {
                label: score 
                for label, score in zip(
                    emotion_results['labels'],
                    emotion_results['scores']
                )
            },
            'semantic_features': semantic_features,
            'text': text
        }
        
        return emotional_representation
    
    def _extract_semantic_features(self, text: str) -> Dict:
        """
        Extract various semantic features from the text
        """
        features = {}
        
        # Analyze intensity (word strength, capitalization, punctuation)
        features['intensity'] = self._analyze_intensity(text)
        
        # Analyze formality (vocabulary, structure)
        features['formality'] = self._analyze_formality(text)
        
        # Analyze certainty (modal verbs, hedging)
        features['certainty'] = self._analyze_certainty(text)
        
        # Analyze urgency (time-related words, imperatives)
        features['urgency'] = self._analyze_urgency(text)
        
        # Analyze sarcasm and irony
        features['sarcasm'] = self._analyze_sarcasm(text)
        features['irony'] = self._analyze_irony(text)
        
        # Analyze ambiguity
        features['ambiguity'] = self._analyze_ambiguity(text)
        
        return features
    
    def _analyze_intensity(self, text: str) -> float:
        """Analyze text intensity based on various factors"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        intensity_words = ['very', 'extremely', 'absolutely', 'totally', 'completely']
        words = text.lower().split()
        intensity_count = sum(1 for word in words if word in intensity_words)
        return min(1.0, intensity_count / len(words))
    
    def _analyze_formality(self, text: str) -> float:
        """Analyze text formality"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        formal_words = ['therefore', 'consequently', 'furthermore', 'however', 'thus']
        words = text.lower().split()
        formal_count = sum(1 for word in words if word in formal_words)
        return min(1.0, formal_count / len(words))
    
    def _analyze_certainty(self, text: str) -> float:
        """Analyze text certainty"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        uncertainty_words = ['maybe', 'perhaps', 'possibly', 'might', 'could']
        words = text.lower().split()
        uncertainty_count = sum(1 for word in words if word in uncertainty_words)
        return 1.0 - min(1.0, uncertainty_count / len(words))
    
    def _analyze_urgency(self, text: str) -> float:
        """Analyze text urgency"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        urgency_words = ['now', 'immediately', 'urgent', 'hurry', 'quick']
        words = text.lower().split()
        urgency_count = sum(1 for word in words if word in urgency_words)
        return min(1.0, urgency_count / len(words))
    
    def _analyze_sarcasm(self, text: str) -> float:
        """Analyze text for sarcasm"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        sarcasm_indicators = ['yeah right', 'sure', 'whatever', 'great', 'wow']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in sarcasm_indicators)
    
    def _analyze_irony(self, text: str) -> float:
        """Analyze text for irony"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        irony_indicators = ['of course', 'naturally', 'obviously', 'clearly']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in irony_indicators)
    
    def _analyze_ambiguity(self, text: str) -> float:
        """Analyze text ambiguity"""
        # Simple implementation - can be enhanced with more sophisticated analysis
        ambiguous_words = ['it', 'this', 'that', 'they', 'them', 'those']
        words = text.lower().split()
        ambiguous_count = sum(1 for word in words if word in ambiguous_words)
        return min(1.0, ambiguous_count / len(words)) 