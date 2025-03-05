# -*- coding: utf-8 -*-
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
