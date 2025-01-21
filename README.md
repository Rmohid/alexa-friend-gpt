# Friend GPT - Your Sophisticated AI Companion

An Alexa skill that lets you chat with GPT, an AI friend who provides thoughtful insights in an elegant British female voice.

## Features

- Sophisticated, nuanced analysis of topics
- Elegant British female voice (Ivy)
- Uses latest GPT model (auto-detected)
- Refined conversation style
- British English spelling
- Comprehensive error handling
- Credit usage monitoring

## Usage

Simply say:
- "Alexa, ask friend gpt about artificial intelligence"
- "Alexa, ask friend gpt to analyse modern literature"
- "Alexa, ask friend gpt about philosophical concepts"

## Skill Structure

This repository follows the Alexa-hosted skills package format:

```
.
├── lambda/
│   ├── lambda_function.py
│   └── requirements.txt
│
└── skill-package/
    ├── interactionModels/
    │   └── custom/
    │       └── en-US.json
    └── skill.json
```

## Setup Instructions

1. Create a new Alexa-hosted skill:
   - Visit the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
   - Click "Create Skill"
   - Name: "Friend GPT"
   - Choose "Custom" model
   - Choose "Alexa-Hosted (Python)"
   - Click "Import skill"
   - Enter this repository's .git URL

2. Set Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key

## Development

This skill is designed to be hosted on Alexa-hosted skills, which provides:
- Free SSL certificate
- AWS Lambda function
- CloudWatch logs
- Auto-scaling

### Local Testing

1. Clone this repository
2. Install dependencies:
   ```bash
   cd lambda
   pip install -r requirements.txt
   ```
3. Set environment variables:
   ```bash
   export OPENROUTER_API_KEY=your_key_here
   ```
4. Run tests:
   ```bash
   python -m unittest test_lambda_function.py
   ```

## Special Features

- **Dynamic Model Selection**: Automatically detects and utilises the latest available GPT model
- **British English**: Consistent use of British spelling and phrasing
- **Sophisticated Style**: Refined, thoughtful responses
- **Memory Management**: Efficient caching of model information
- **Error Recovery**: Graceful fallback to stable model versions

## Error Handling

The skill provides clear, polite feedback for different scenarios:

1. API Key Issues:
   - "I do apologise, but I seem to be missing my configuration. Perhaps the skill administrator could assist?"

2. Credit-Related Errors:
   - "I do apologise, but I'm unable to assist at the moment. Might we continue our chat later?"

3. General Errors:
   - "I do apologise, but I'm having a bit of trouble with that. Might we try again?"

## Part of the AI Friends Series

This skill is part of a series of AI friend skills:
- [Friend DeepSeek](https://github.com/Rmohid/alexa-friend-deepseek) - Educational explanations
- [Friend Grok](https://github.com/Rmohid/alexa-friend-grok) - Simple, fun explanations
- Friend GPT (this skill) - Sophisticated insights

## Licence

MIT Licence