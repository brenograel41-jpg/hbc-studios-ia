"""
GHS STUDIOS IA - Core ChatBot Logic
Manages AI model selection and conversations
"""

import os
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AIProvider:
    """Base class for AI providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat(self, message: str, history: List[Dict] = None) -> str:
        """Send message and get response"""
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    """OpenAI GPT Models (Paid/Free tier)"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key)
        self.model = model
        try:
            import openai
            openai.api_key = api_key
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            logger.error("openai library not installed")
            raise
    
    def chat(self, message: str, history: List[Dict] = None) -> str:
        try:
            messages = history or []
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=float(os.getenv('TEMPERATURE', 0.7)),
                max_tokens=int(os.getenv('MAX_TOKENS', 2000))
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise


class GoogleGeminiProvider(AIProvider):
    """Google Gemini (Free tier available)"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            logger.error("google-generativeai library not installed")
            raise
    
    def chat(self, message: str, history: List[Dict] = None) -> str:
        try:
            if history:
                chat = self.model.start_chat(history=history)
                response = chat.send_message(message)
            else:
                response = self.model.generate_content(message)
            
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini error: {e}")
            raise


class AnthropicProvider(AIProvider):
    """Anthropic Claude (Paid)"""
    
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        super().__init__(api_key)
        self.model = model
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            logger.error("anthropic library not installed")
            raise
    
    def chat(self, message: str, history: List[Dict] = None) -> str:
        try:
            messages = history or []
            messages.append({"role": "user", "content": message})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=int(os.getenv('MAX_TOKENS', 2000)),
                messages=messages
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise


class CohereProvider(AIProvider):
    """Cohere API (Paid)"""
    
    def __init__(self, api_key: str, model: str = "command"):
        super().__init__(api_key)
        self.model = model
        try:
            import cohere
            self.client = cohere.Client(api_key)
        except ImportError:
            logger.error("cohere library not installed")
            raise
    
    def chat(self, message: str, history: List[Dict] = None) -> str:
        try:
            chat_history = []
            if history:
                for msg in history:
                    chat_history.append({
                        "role": msg["role"],
                        "message": msg["content"]
                    })
            
            response = self.client.chat(
                message=message,
                chat_history=chat_history,
                model=self.model
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Cohere error: {e}")
            raise


class ChatBot:
    """Main ChatBot class"""
    
    def __init__(self, model: str = None):
        self.model = model or os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
        self.history: List[Dict] = []
        self.max_history = int(os.getenv('MAX_HISTORY', 50))
        self.provider = self._initialize_provider()
        
        logger.info(f"ChatBot initialized with model: {self.model}")
    
    def _initialize_provider(self) -> AIProvider:
        """Initialize the appropriate AI provider"""
        
        if 'gpt' in self.model.lower():
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            return OpenAIProvider(api_key, self.model)
        
        elif 'gemini' in self.model.lower() or self.model == 'google':
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not configured")
            return GoogleGeminiProvider(api_key)
        
        elif 'claude' in self.model.lower():
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            return AnthropicProvider(api_key, self.model)
        
        elif 'cohere' in self.model.lower() or self.model == 'command':
            api_key = os.getenv('COHERE_API_KEY')
            if not api_key:
                raise ValueError("COHERE_API_KEY not configured")
            return CohereProvider(api_key, self.model)
        
        else:
            raise ValueError(f"Unknown model: {self.model}")
    
    def chat(self, message: str) -> str:
        """Send a message and get response"""
        try:
            self.history.append({
                "role": "user",
                "content": message
            })
            
            response = self.provider.chat(message, self.history)
            
            self.history.append({
                "role": "assistant",
                "content": response
            })
            
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.history.copy()
    
    def switch_model(self, model: str):
        """Switch to a different AI model"""
        self.model = model
        self.provider = self._initialize_provider()
        logger.info(f"Switched to model: {model}")
    
    def export_conversation(self, filename: str = None) -> str:
        """Export conversation to JSON"""
        if filename is None:
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
            "history": self.history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Conversation exported to {filename}")
        return filename