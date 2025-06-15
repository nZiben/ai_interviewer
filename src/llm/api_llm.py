import requests
from typing import Optional
import json

class API_LLM:
    def __init__(self, endpoint: str, api_key: str):
        """
        Initialize the API-based Language Model service.
        
        Args:
            endpoint (str): The API endpoint URL
            api_key (str): API key for authentication
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_answer(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate a response using the language model API.
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum number of tokens in the response
            
        Returns:
            Optional[str]: Generated response or None if generation fails
        """
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                print(f"Error in generation: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            return None 