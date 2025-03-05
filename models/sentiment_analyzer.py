class SentimentAnalyzer:
    def __init__(self, api_client):
        self.api_client = api_client
        
    def analyze(self, text, context=None):
        """
        Analyze text considering literal meaning, appropriate machine reaction,
        and previous conversation context
        """
        # Prepare context for API
        context_data = self._prepare_context(context) if context else {}
        
        # Get analysis from DeepSeek API
        analysis_result = self.api_client.analyze_text(
            text=text,
            context=context_data
        )
        
        # Extract and structure the results
        result = {
            "literal_meaning": analysis_result.get("meaning", ""),
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "sentiment_score": analysis_result.get("sentiment_score", 0.0),
            "suggested_reaction": analysis_result.get("machine_reaction", "neutral"),
            "confidence": analysis_result.get("confidence", 0.0),
            "entities": analysis_result.get("entities", []),
            "intent": analysis_result.get("intent", "")
        }
        
        return result
        
    def _prepare_context(self, context):
        """Format context data for the API request"""
        if not context or not context.conversation_history:
            return {}
            
        # Format conversation history for API
        history = []
        for entry in context.conversation_history:
            history.append({
                "text": entry["user_input"],
                "reaction": entry["machine_reaction"],
                "sentiment": entry["sentiment"]
            })
            
        return {
            "conversation_history": history,
            "current_emotion": context.current_emotion,
            "current_topic": context.current_topic
        }