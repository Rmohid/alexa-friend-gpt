#!/usr/bin/env python3

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import requests
import json
import os
import sys
from datetime import datetime, timedelta

# Cache for model information
model_cache = {
    'timestamp': None,
    'model': None
}

def get_latest_model():
    """Get the latest GPT model from OpenRouter API"""
    # Check cache first (cache valid for 1 hour)
    if (model_cache['timestamp'] and 
        model_cache['model'] and 
        datetime.now() - model_cache['timestamp'] < timedelta(hours=1)):
        return model_cache['model']

    try:
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            raise Exception("API key not configured")

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        response = requests.get(
            'https://openrouter.ai/api/v1/models',
            headers=headers
        )
        response.raise_for_status()
        
        models = response.json()
        
        # Find the latest GPT chat model
        chat_models = [
            model for model in models 
            if model['id'].startswith('openai/') and 
            'chat' in model.get('capabilities', [])
        ]
        
        if not chat_models:
            raise Exception("No GPT chat models found")
            
        # Sort by created_at if available, otherwise use the first one
        latest_model = sorted(
            chat_models,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )[0]['id']

        # Update cache
        model_cache['timestamp'] = datetime.now()
        model_cache['model'] = latest_model
        
        return latest_model
        
    except Exception as e:
        # Fallback model if API call fails
        return 'openai/gpt-4-1106-preview'

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "LaunchRequest"

    def handle(self, handler_input):
        speak_output = ("Hello! I'm your GPT friend, delighted to assist you today. "
                       "I rather enjoy thoughtful discussions on any topic you fancy. "
                       "What shall we explore together?")
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What would you like to discuss?")
                .response
        )

class AskGPTIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and \
               handler_input.request_envelope.request.intent.name == "AskIntent"

    def format_response(self, text):
        """Format response with SSML voice"""
        return f'<speak><voice name="Ivy">{text}</voice></speak>'

    def handle(self, handler_input):
        try:
            # Get the prompt from the slot value
            slots = handler_input.request_envelope.request.intent.slots
            prompt = slots["prompt"].value

            # Get API key from environment
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if not api_key:
                return (
                    handler_input.response_builder
                        .speak(self.format_response(
                            "I do apologise, but I seem to be missing my configuration. Perhaps the skill administrator could assist?"
                        ))
                        .response
                )

            # Get the latest model
            model_name = get_latest_model()

            # Prepare API request
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:3000',
            }

            data = {
                'model': model_name,
                'messages': [{'role': 'user', 'content': prompt}]
            }

            # Make API request
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            # Check for credit-related errors
            if response.status_code == 402 or response.status_code == 429:
                error_data = response.json()
                if any(keyword in str(error_data).lower() for keyword in ['credit', 'quota', 'payment', 'billing']):
                    return (
                        handler_input.response_builder
                            .speak(self.format_response(
                                "I do apologise, but I'm unable to assist at the moment. Might we continue our chat later?"
                            ))
                            .response
                    )
            
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            response_text = result['choices'][0]['message']['content']

            # Format response for Alexa with appropriate voice and follow-up
            speak_output = self.format_response(
                f"{response_text} Shall we explore another topic?"
            )
            
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("What else would you like to discuss?")
                    .response
            )

        except Exception as e:
            speak_output = self.format_response(
                "I do apologise, but I'm having a bit of trouble with that. Might we try again?"
            )
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("What would you like to know?")
                    .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and \
               handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent"

    def handle(self, handler_input):
        speak_output = ("I'm your GPT friend, and I'd be delighted to engage in thoughtful discussions "
                       "on any topic that interests you. Whether it's literature, science, philosophy, or "
                       "current events, I'm quite well-versed in a variety of subjects. "
                       "Perhaps you'd like to ask about 'the impact of artificial intelligence on society' or "
                       "'the most influential books in history'? What piques your interest?")
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What would you like to explore?")
                .response
        )

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and \
               (handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent" or
                handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent")

    def handle(self, handler_input):
        speak_output = "It's been a pleasure chatting. Do come back when you'd like another enlightening conversation!"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

# Build the skill
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AskGPTIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
handler = sb.lambda_handler()