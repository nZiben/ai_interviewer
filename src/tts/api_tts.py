import requests
from typing import Optional
import json
import os

class API_TTS:
    def __init__(self, endpoint: str, api_key: str):
        """
        Initialize the API-based Text-to-Speech service.
        
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
    
    def synthesize(self, text: str, output_path: str, voice: str = "default") -> bool:
        """
        Synthesize text to speech using the API.
        
        Args:
            text (str): Text to synthesize
            output_path (str): Path where the audio file will be saved
            voice (str): Voice to use for synthesis
            
        Returns:
            bool: True if synthesis was successful, False otherwise
        """
        try:
            payload = {
                "text": text,
                "voice": voice
            }
            
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                # Assuming the API returns audio data directly
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"Error in synthesis: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error during synthesis: {str(e)}")
            return False 