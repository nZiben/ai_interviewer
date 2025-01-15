"""Google Cloud Speech-to-Text"""
import os
from google.cloud import speech

class GoogleSTT:
    def __init__(self, credentials_json: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_json
        self.client = speech.SpeechClient()

    def speech_to_text(self, audio_data: bytes) -> str:
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            language_code="en-US"
        )
        try:
            response = self.client.recognize(config=config, audio=audio)
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            return transcript.strip()
        except Exception as e:
            return f"[Google STT Error]: {str(e)}"
