class EmotionMapper:
    def __init__(self):
        # Define emotion mappings and thresholds
        self.emotion_map = {
            "threat": ["scared", "defensive", "cautious", "alarmed", "threatened"],
            "positive": ["happy", "excited", "pleased", "joyful", "delighted", "grateful"],
            "negative": ["sad", "disappointed", "concerned", "upset", "frustrated", "angry"],
            "question": ["curious", "helpful", "attentive", "interested"],
            "neutral": ["calm", "neutral", "balanced", "composed", "collected"]
        }
        
        # Define emotion transition rules
        self.transition_rules = {
            # From scared to other emotions
            "scared": {
                "positive": "cautiously_optimistic",
                "negative": "fearful",
                "neutral": "wary",
                "question": "hesitant"
            },
            # From happy to other emotions
            "happy": {
                "threat": "concerned",
                "negative": "sympathetic",
                "neutral": "content",
                "question": "eager_to_help"
            },
            # From sad to other emotions
            "sad": {
                "threat": "anxious",
                "positive": "hopeful",
                "neutral": "reflective",
                "question": "willing_to_help"
            },
            # From neutral to other emotions
            "neutral": {
                "threat": "alert",
                "positive": "pleased",
                "negative": "concerned",
                "question": "attentive"
            }
        }
        
    def map_sentiment_to_emotion(self, sentiment_data, context):
        """
        Map sentiment analysis results to machine emotion considering:
        1. Literal meaning of text
        2. Appropriate machine reaction
        3. Previous emotional state
        """
        # Get sentiment and intensity from analysis
        sentiment = sentiment_data.get('sentiment', 'neutral')
        intensity = sentiment_data.get('intensity', 0)
        is_subjective = sentiment_data.get('is_subjective', False)
        
        # Map sentiment to base emotion
        if sentiment == "positive":
            if intensity > 0.5:
                base_emotion = "excited"
            else:
                base_emotion = "happy"
        elif sentiment == "negative":
            if intensity > 0.5:
                base_emotion = "angry"
            else:
                base_emotion = "sad"
        else:
            base_emotion = "neutral"
            
        # Adjust emotion based on subjectivity
        if is_subjective:
            if base_emotion == "neutral":
                base_emotion = "calm"
            elif base_emotion == "happy":
                base_emotion = "excited"
            elif base_emotion == "sad":
                base_emotion = "frustrated"
                
        # If no previous context, return the base emotion
        if not context or not context.emotion_history:
            return base_emotion
            
        # Get previous emotion
        previous_emotion = context.current_emotion
        
        # Apply transition rules for smoother emotion changes
        if previous_emotion in self.transition_rules:
            transition_map = self.transition_rules[previous_emotion]
            
            # Find the emotion category for the base emotion
            category = self._find_category(base_emotion)
            
            if category in transition_map:
                # Return transitional emotion
                return transition_map[category]
        
        # If no transition rule applies, return base emotion
        return base_emotion
        
    def _find_category(self, emotion):
        """Find which category an emotion belongs to"""
        for category, emotions in self.emotion_map.items():
            if emotion in emotions:
                return category
        return "neutral"