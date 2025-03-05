"""
Configuration settings for the sentiment analysis application
"""

# Sentiment Analysis settings
POLARITY_THRESHOLD = 0.1  # Lower threshold for more sensitive sentiment detection
SUBJECTIVITY_THRESHOLD = 0.3  # Lower threshold for better subjectivity detection

# Context settings
MEMORY_LENGTH = 5  # Number of conversation turns to remember
CONTEXT_DECAY_FACTOR = 0.8  # How quickly previous context loses importance
MAX_CONTEXT_LENGTH = 1000  # Maximum characters to store in context

# Emotion settings
DEFAULT_EMOTION = "neutral"
EMOTION_TRANSITION_THRESHOLD = 0.3  # Minimum score difference to trigger emotion change
EMOTION_SMOOTHING_FACTOR = 0.7  # How quickly emotions transition
SUPPORTED_EMOTIONS = [
    "happy", "sad", "angry", "neutral", "excited", "calm",
    "frustrated", "surprised", "worried", "confident"
]

# Response settings
RESPONSE_TEMPERATURE = 0.7  # Controls randomness in response generation
MAX_RESPONSE_LENGTH = 150  # Maximum length of generated responses
MIN_RESPONSE_LENGTH = 20  # Minimum length of generated responses
RESPONSE_PERSONALITY = "friendly"  # Overall personality of the chatbot

# Logging settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "emotion_analyzer.log"  # Log file path

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 60  # Maximum API requests per minute
REQUEST_DELAY = 1.0  # Delay between requests in seconds