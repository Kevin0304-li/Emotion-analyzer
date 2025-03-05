# Emotion Analyzer

A Python-based chatbot that analyzes emotions in text using VADER sentiment analysis. The chatbot can detect various emotions and respond appropriately based on the user's input.

## Features

- Emotion detection using VADER sentiment analysis
- Support for multiple emotions:
  - Positive: ecstatic, excited, happy, pleased
  - Negative: furious, angry, frustrated, annoyed
  - Sad: devastated, sad, disappointed, down
  - Neutral: calm, thoughtful, curious
- Context-aware responses
- Natural language interaction

## Requirements

- Python 3.x
- NLTK
- VADER sentiment analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kevin0304-li/Emotion-analyzer.git
cd Emotion-analyzer
```

2. Install required packages:
```bash
pip install nltk
```

3. Run the chatbot:
```bash
python app.py
```

## Usage

1. Start the chatbot by running `python app.py`
2. Type your message and press Enter
3. The chatbot will analyze your message and respond with an appropriate emotion-based response
4. Type 'exit' to quit the chatbot

## Example Interactions

```
> I'm so happy about my new job!
[excited] That's amazing! I'm thrilled to hear that!

> This is making me really angry
[angry] I can see why you're angry. That's completely understandable.

> I feel sad about what happened
[sad] I'm sorry to hear that. Let me know if you want to talk about it.
```

## Project Structure

- `app.py`: Main application file containing the VADER sentiment analyzer and chatbot logic
- `responses/response_generator.py`: Response generation module with emotion-based responses
- `README.md`: Project documentation

## License

This project is open source and available under the MIT License. 