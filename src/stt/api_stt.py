import requests
from typing import Optional
import json

class API_STT:
    def __init__(self, endpoint: str, api_key: str):
        """
        Initialize the API-based Speech-to-Text service.
        
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
    
    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio file to text using the API.
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            Optional[str]: Transcribed text or None if transcription fails
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {'file': audio_file}
                response = requests.post(
                    self.endpoint,
                    headers=self.headers,
                    files=files
                )
                
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                print(f"Error in transcription: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None 