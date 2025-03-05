import json
import requests
from config import DEEPSEEK_API_URL, DEEPSEEK_MODEL, RESPONSE_TEMPERATURE, MAX_RESPONSE_LENGTH

class DeepSeekClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = DEEPSEEK_API_URL
        self.model = DEEPSEEK_MODEL
        
    def analyze_text(self, text, context=None):
        """
        Send text to DeepSeek API for sentiment analysis with context
        """
        # Prepare the prompt to include context information
        prompt = self._build_analysis_prompt(text, context)
        
        # Call DeepSeek API
        response = self._call_api(prompt, json_output=True)
        
        # Parse and structure the response
        return self._parse_analysis_response(response)
        
    def generate_text(self, prompt):
        """
        Generate text using DeepSeek API
        """
        response = self._call_api(
            prompt, 
            temperature=RESPONSE_TEMPERATURE,
            max_tokens=MAX_RESPONSE_LENGTH
        )
        
        return response.strip()
        
    def _build_analysis_prompt(self, text, context=None):
        """Build a prompt that includes context for better analysis"""
        prompt = "Analyze the following text for sentiment, meaning, and appropriate machine reaction:\n\n"
        prompt += f"TEXT: {text}\n\n"
        
        if context and context.get("conversation_history"):
            prompt += "CONVERSATION HISTORY:\n"
            for i, entry in enumerate(context["conversation_history"]):
                prompt += f"[{i+1}] User: {entry['text']}\n"
                prompt += f"    Machine reaction: {entry['reaction']}\n"
            
            prompt += f"\nCurrent machine emotion: {context.get('current_emotion', 'neutral')}\n"
            
        prompt += "\nProvide analysis in JSON format with the following fields:\n"
        prompt += "- meaning: literal interpretation of the text\n"
        prompt += "- sentiment: positive, negative, neutral, or other appropriate label\n"
        prompt += "- sentiment_score: numerical score from -1.0 to 1.0\n"
        prompt += "- machine_reaction: how the machine should emotionally react\n"
        prompt += "- confidence: confidence score for the analysis\n"
        prompt += "- entities: key entities mentioned in the text\n"
        prompt += "- intent: user's apparent intent (question, statement, command, etc.)\n"
        
        return prompt
        
    def _call_api(self, prompt, temperature=0.3, max_tokens=500, json_output=False):
        """Make the actual API call to DeepSeek"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if json_output:
            data["response_format"] = {"type": "json_object"}
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                print(response.text)
                return self._get_fallback_response(json_output)
                
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            return self._get_fallback_response(json_output)
    
    def _parse_analysis_response(self, response_text):
        """Parse the API response into a structured format"""
        try:
            # Try to parse as JSON
            result = json.loads(response_text)
            
            # Ensure all expected fields are present
            default_result = {
                "meaning": "",
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "machine_reaction": "neutral",
                "confidence": 0.0,
                "entities": [],
                "intent": "statement"
            }
            
            # Update with actual values from response
            for key in default_result:
                if key in result:
                    default_result[key] = result[key]
                    
            return default_result
            
        except json.JSONDecodeError:
            print("Failed to parse API response as JSON")
            return {
                "meaning": "Unable to analyze text",
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "machine_reaction": "confused",
                "confidence": 0.0,
                "entities": [],
                "intent": "unknown"
            }
    
    def _get_fallback_response(self, json_output=False):
        """Return a fallback response when API call fails"""
        if json_output:
            return json.dumps({
                "meaning": "API error occurred",
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "machine_reaction": "confused",
                "confidence": 0.0,
                "entities": [],
                "intent": "unknown"
            })
        else:
            return "I'm having trouble processing that right now. Could you try again?"