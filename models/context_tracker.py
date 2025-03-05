import time

class ContextTracker:
    def __init__(self, memory_length=5):
        self.conversation_history = []
        self.emotion_history = []
        self.memory_length = memory_length
        self.current_emotion = "neutral"
        self.current_topic = None
        
    def update(self, user_input, sentiment_result, machine_reaction):
        """
        Update conversation context with new input, sentiment and machine reaction
        """
        # Store the full context tuple
        context_entry = {
            "user_input": user_input,
            "literal_meaning": sentiment_result.get("meaning", ""),
            "sentiment": sentiment_result.get("sentiment", "neutral"),
            "sentiment_score": sentiment_result.get("sentiment_score", 0.0),
            "machine_reaction": machine_reaction,
            "timestamp": time.time()
        }
        
        # Update conversation history
        self.conversation_history.append(context_entry)
        if len(self.conversation_history) > self.memory_length:
            self.conversation_history.pop(0)
            
        # Update emotion history
        self.emotion_history.append(machine_reaction)
        if len(self.emotion_history) > self.memory_length:
            self.emotion_history.pop(0)
            
        # Update current emotion
        self.current_emotion = machine_reaction
        
        # Try to identify current topic
        self._update_topic(user_input, sentiment_result)
        
    def _update_topic(self, user_input, sentiment_result):
        """Attempt to identify or update the conversation topic"""
        # Simple topic extraction from entities
        entities = sentiment_result.get("entities", [])
        if entities:
            # Use the most prominent entity as the topic
            self.current_topic = entities[0]
        
    def get_context_summary(self):
        """
        Return a summary of the current context for response generation
        """
        if not self.conversation_history:
            return {
                "current_emotion": self.current_emotion,
                "current_topic": None,
                "conversation_summary": "This is the beginning of the conversation."
            }
            
        # Create a summary of recent conversation
        recent_exchanges = []
        for entry in self.conversation_history:
            recent_exchanges.append({
                "user_input": entry["user_input"],
                "machine_reaction": entry["machine_reaction"]
            })
            
        return {
            "current_emotion": self.current_emotion,
            "current_topic": self.current_topic,
            "conversation_history": recent_exchanges,
            "emotion_history": self.emotion_history
        }