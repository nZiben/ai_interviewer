"""Google Cloud Text-to-Speech Integration"""
import os
from google.cloud import texttospeech

class GoogleTTS:
    def __init__(self, credentials_json: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_json
        self.client = texttospeech.TextToSpeechClient()

    def text_to_speech(self, text: str) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return response.audio_content
