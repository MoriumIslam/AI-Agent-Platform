"""
Response Generator Agent
Generates AI-powered replies using OpenAI GPT API
Includes confidence scoring, human review routing, and fallback mechanisms
"""

import os
import logging
import json
from typing import Optional
import random

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generate responses using LLM"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "sk-test-demo")
        self.model = "gpt-4"  # or gpt-3.5-turbo for cost optimization
        self.timeout_seconds = 30
    
    def get_system_prompt(self, brand_voice: str = "professional") -> str:
        """Get system prompt for LLM"""
        
        prompts = {
            "professional": "You are a professional customer support representative. Write concise, helpful responses.",
            "friendly": "You are a friendly customer support representative. Be warm and approachable.",
            "technical": "You are a technical support specialist. Provide detailed, accurate solution information."
        }
        
        return prompts.get(brand_voice, prompts["professional"])
    
    def generate_response(self, text: str, brand_voice: str = "professional") -> dict:
        """
        Generate a response for a message
        In production, integrate with OpenAI API
        
        Returns: {response_text, confidence, should_post, tokens_used}
        """
        
        try:
            # Simulated response generation (in production, call OpenAI API)
            system_prompt = self.get_system_prompt(brand_voice)
            
            # In production:
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": text}
            #     ],
            #     temperature=0.7,
            #     max_tokens=100,
            #     timeout=self.timeout_seconds
            # )
            
            # Simulated responses based on input
            response_text = self._generate_simulated_response(text)
            
            # Calculate confidence
            confidence = self._calculate_confidence(text, response_text)
            
            # Determine if should auto-post
            should_post = confidence > 0.80
            
            logger.info(f"✅ Response generated: {response_text[:50]}... (confidence: {confidence:.2%})")
            
            return {
                "response_text": response_text,
                "confidence": round(confidence, 2),
                "should_post": should_post,
                "action": "auto_post" if should_post else "human_review",
                "model_used": self.model,
                "tokens_used": self._estimate_tokens(text + response_text)
            }
        
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self._get_fallback_response(text)
    
    def _generate_simulated_response(self, text: str) -> str:
        """Generate simulated response for demo"""
        
        templates = {
            "greeting": "Thanks for reaching out! We appreciate your interest. How can we help you today?",
            "feature_question": "Great question! That feature is available in our Pro plan. Would you like more details?",
            "support": "We're here to help! Can you provide more details about your issue?",
            "pricing": "Thanks for your interest! You can find our pricing on our website. Would you like a demo?",
            "technical": "Thanks for reporting this! Our team is investigating. We'll have an update soon.",
        }
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["hello", "hi", "thanks", "thank"]):
            return templates["greeting"]
        elif any(word in text_lower for word in ["feature", "how", "can", "way"]):
            return templates["feature_question"]
        elif any(word in text_lower for word in ["help", "problem", "issue", "bug"]):
            return templates["support"]
        elif any(word in text_lower for word in ["price", "pricing", "cost", "subscription"]):
            return templates["pricing"]
        elif any(word in text_lower for word in ["error", "broken", "not working"]):
            return templates["technical"]
        else:
            return templates["greeting"]
    
    def _calculate_confidence(self, text: str, response: str) -> float:
        """
        Calculate confidence score for response
        Factors: response length, text clarity, brand guidelines
        """
        
        confidence = 0.5  # Base confidence
        
        # Response is reasonable length
        if 20 < len(response) < 200:
            confidence += 0.25
        
        # Input is clear and well-formed
        if len(text.split()) > 3:
            confidence += 0.15
        
        # Response doesn't contain prohibited content
        if not any(word in response.lower() for word in ["password", "secret", "apikey"]):
            confidence += 0.10
        
        return min(0.99, confidence)
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Average: 1 token ≈ 4 characters
        return len(text) // 4
    
    def _get_fallback_response(self, text: str) -> dict:
        """Get fallback response if LLM fails"""
        
        return {
            "response_text": "Thanks for reaching out! A team member will respond shortly.",
            "confidence": 0.60,
            "should_post": False,  # Require human review for fallback
            "action": "human_review",
            "model_used": "fallback_template",
            "tokens_used": 0,
            "error": "LLM timeout, using template"
        }

# ============= SINGLETON =============

_generator = ResponseGenerator()

def generate_reply(text: str, brand_voice: str = "professional") -> dict:
    """Generate a reply (convenience function)"""
    return _generator.generate_response(text, brand_voice)
