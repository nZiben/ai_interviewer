"""ElevenLabs TTS Integration"""
import os
from elevenlabs import generate, set_api_key

class ElevenLabsTTS:
    def __init__(self, api_key: str):
        set_api_key(api_key)

    def text_to_speech(self, text: str) -> bytes:
        try:
            audio = generate(text=text, voice='Bella', model='eleven_monolingual_v1')
            return audio
        except Exception as e:
            return b""
