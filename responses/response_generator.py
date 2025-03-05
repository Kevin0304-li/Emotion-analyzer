# -*- coding: utf-8 -*-
from typing import Dict, Optional
import random

class ResponseGenerator:
    def __init__(self):
        self.responses = {
            # Positive emotions
            'ecstatic': [
                "That's absolutely amazing! I'm thrilled to hear that!",
                "Wow, that's incredible! I'm so excited for you!",
                "This is fantastic news! I'm overjoyed to hear that!",
                "That's absolutely wonderful! I'm ecstatic for you!"
            ],
            'excited': [
                "That's great news! I'm excited to hear that!",
                "How exciting! That's wonderful to hear!",
                "That's amazing! I'm so excited for you!",
                "This is so exciting! I'm happy to hear that!"
            ],
            'happy': [
                "I'm glad you're happy! That's wonderful!",
                "That's great to hear! I'm happy for you!",
                "I'm so glad you're feeling happy!",
                "That makes me happy to hear!"
            ],
            'pleased': [
                "I'm pleased to hear that!",
                "That's good to hear!",
                "I'm glad you're pleased!",
                "That's wonderful to hear!"
            ],
            'grateful': [
                "I'm grateful to hear you're feeling that way!",
                "That's a wonderful feeling of gratitude!",
                "I'm thankful to hear that!",
                "That's such a grateful attitude!"
            ],
            'proud': [
                "You should be proud! That's amazing!",
                "I'm proud of you too!",
                "That's something to be proud of!",
                "You have every right to be proud!"
            ],
            'optimistic': [
                "That's a great optimistic outlook!",
                "I love your optimistic attitude!",
                "That's wonderful optimism!",
                "Your optimism is inspiring!"
            ],
            'inspired': [
                "That's truly inspiring!",
                "Your inspiration is contagious!",
                "That's wonderful to be inspired!",
                "I'm inspired by your enthusiasm!"
            ],
            'confident': [
                "Your confidence is admirable!",
                "That's great confidence!",
                "I love your confident attitude!",
                "Your confidence is inspiring!"
            ],
            'peaceful': [
                "That's a wonderful peaceful feeling!",
                "I'm glad you're feeling peaceful!",
                "That's such a peaceful state of mind!",
                "Peace is a beautiful feeling!"
            ],
            
            # Negative emotions
            'furious': [
                "I can see why you're furious. That's completely understandable.",
                "Your anger is justified. That's really frustrating.",
                "I understand your fury. That's really upsetting.",
                "That's definitely something to be furious about."
            ],
            'angry': [
                "I understand why you're angry. That's frustrating.",
                "Your anger is understandable. That's upsetting.",
                "I can see why you're angry. That's not fair.",
                "That's definitely something to be angry about."
            ],
            'frustrated': [
                "I understand your frustration. That's really annoying.",
                "That's definitely frustrating. I hear you.",
                "I can see why you're frustrated. That's difficult.",
                "Your frustration is completely understandable."
            ],
            'annoyed': [
                "That's definitely annoying. I understand.",
                "I can see why you're annoyed. That's frustrating.",
                "That's really annoying. I hear you.",
                "Your annoyance is justified."
            ],
            'anxious': [
                "I understand your anxiety. That's really stressful.",
                "That's definitely anxiety-inducing. I hear you.",
                "I can see why you're anxious. That's concerning.",
                "Your anxiety is understandable."
            ],
            'worried': [
                "I understand your worry. That's concerning.",
                "That's definitely worrying. I hear you.",
                "I can see why you're worried. That's stressful.",
                "Your worry is justified."
            ],
            'overwhelmed': [
                "I understand feeling overwhelmed. That's a lot to handle.",
                "That's definitely overwhelming. I hear you.",
                "I can see why you're overwhelmed. That's stressful.",
                "Being overwhelmed is completely understandable."
            ],
            'stressed': [
                "I understand your stress. That's really difficult.",
                "That's definitely stressful. I hear you.",
                "I can see why you're stressed. That's overwhelming.",
                "Your stress is completely understandable."
            ],
            'irritated': [
                "I understand your irritation. That's frustrating.",
                "That's definitely irritating. I hear you.",
                "I can see why you're irritated. That's annoying.",
                "Your irritation is justified."
            ],
            'disappointed': [
                "I understand your disappointment. That's really hard.",
                "That's definitely disappointing. I hear you.",
                "I can see why you're disappointed. That's upsetting.",
                "Your disappointment is completely understandable."
            ],
            
            # Sad emotions
            'devastated': [
                "I'm so sorry you're feeling devastated. That's really hard.",
                "That's absolutely devastating. I'm here for you.",
                "I can't imagine how devastated you must feel.",
                "I'm here to support you through this devastation."
            ],
            'heartbroken': [
                "I'm so sorry you're heartbroken. That's really painful.",
                "That's absolutely heartbreaking. I'm here for you.",
                "I can't imagine how heartbroken you must feel.",
                "I'm here to support you through this heartbreak."
            ],
            'sad': [
                "I'm sorry you're feeling sad. That's really hard.",
                "That's really sad. I'm here for you.",
                "I understand your sadness. That's difficult.",
                "I'm here to support you through this sadness."
            ],
            'lonely': [
                "I understand feeling lonely. That's really hard.",
                "That's really lonely. I'm here for you.",
                "I can see why you're feeling lonely. That's difficult.",
                "I'm here to keep you company."
            ],
            'grief': [
                "I'm so sorry for your grief. That's really painful.",
                "That's absolutely heartbreaking. I'm here for you.",
                "I can't imagine the grief you must be feeling.",
                "I'm here to support you through your grief."
            ],
            'melancholic': [
                "I understand your melancholy. That's really hard.",
                "That's really melancholic. I'm here for you.",
                "I can see why you're feeling melancholic. That's difficult.",
                "I'm here to support you through this melancholy."
            ],
            'nostalgic': [
                "Nostalgia can be bittersweet. I understand.",
                "That's a nostalgic feeling. I hear you.",
                "I can see why you're feeling nostalgic. That's touching.",
                "Nostalgia can bring up many emotions."
            ],
            'homesick': [
                "I understand feeling homesick. That's really hard.",
                "That's really homesick. I'm here for you.",
                "I can see why you're feeling homesick. That's difficult.",
                "I'm here to support you through this homesickness."
            ],
            
            # Complex emotions
            'confused': [
                "I understand your confusion. That's really puzzling.",
                "That's definitely confusing. Let's figure it out together.",
                "I can see why you're confused. That's complicated.",
                "Let's try to understand this together."
            ],
            'surprised': [
                "That's really surprising! I understand your reaction.",
                "What a surprise! That's unexpected.",
                "I can see why you're surprised. That's unexpected.",
                "That's definitely surprising!"
            ],
            'shocked': [
                "I understand your shock. That's really unexpected.",
                "That's definitely shocking. I hear you.",
                "I can see why you're shocked. That's surprising.",
                "That's absolutely shocking!"
            ],
            'amazed': [
                "That's really amazing! I understand your wonder.",
                "How amazing! That's incredible.",
                "I can see why you're amazed. That's wonderful.",
                "That's absolutely amazing!"
            ],
            'puzzled': [
                "I understand your puzzlement. That's really confusing.",
                "That's definitely puzzling. Let's figure it out.",
                "I can see why you're puzzled. That's complicated.",
                "Let's try to solve this puzzle together."
            ],
            'curious': [
                "That's really interesting! I understand your curiosity.",
                "How fascinating! That's intriguing.",
                "I can see why you're curious. That's interesting.",
                "That's definitely worth exploring!"
            ],
            'thoughtful': [
                "That's really thoughtful of you to consider that.",
                "How thoughtful! That's considerate.",
                "I can see you're being thoughtful. That's kind.",
                "That's a very thoughtful perspective!"
            ],
            'contemplative': [
                "I understand your contemplation. That's deep.",
                "That's definitely worth contemplating.",
                "I can see you're being contemplative. That's profound.",
                "That's a contemplative moment."
            ],
            'reflective': [
                "I understand your reflection. That's meaningful.",
                "That's definitely worth reflecting on.",
                "I can see you're being reflective. That's thoughtful.",
                "That's a reflective moment."
            ],
            
            # Neutral emotions
            'calm': [
                "That's a wonderful calm feeling!",
                "I'm glad you're feeling calm!",
                "That's such a peaceful calm!",
                "Calm is a beautiful state of mind!"
            ],
            'focused': [
                "That's great focus! Keep it up!",
                "I love your focused attitude!",
                "That's wonderful concentration!",
                "Your focus is admirable!"
            ],
            'determined': [
                "That's great determination!",
                "I love your determined attitude!",
                "That's wonderful perseverance!",
                "Your determination is inspiring!"
            ],
            'mindful': [
                "That's wonderful mindfulness!",
                "I love your mindful approach!",
                "That's great awareness!",
                "Your mindfulness is admirable!"
            ],
            'attentive': [
                "That's great attentiveness!",
                "I love your attentive attitude!",
                "That's wonderful awareness!",
                "Your attentiveness is admirable!"
            ],
            'observant': [
                "That's great observation!",
                "I love your observant nature!",
                "That's wonderful attention to detail!",
                "Your observation skills are impressive!"
            ],
            'patient': [
                "That's great patience!",
                "I love your patient attitude!",
                "That's wonderful tolerance!",
                "Your patience is admirable!"
            ],
            'balanced': [
                "That's great balance!",
                "I love your balanced approach!",
                "That's wonderful equilibrium!",
                "Your balance is admirable!"
            ]
        }

    def generate_response(self, emotion: str, user_input: str) -> str:
        """Generate a response based on the detected emotion."""
        if emotion in self.responses:
            return random.choice(self.responses[emotion])
        return "I understand how you're feeling."
