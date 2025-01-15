"""Mozilla TTS Integration (примерно как Coqui)"""
import tempfile
from TTS.api import TTS

class MozillaTTS:
    def __init__(self, model_name='tts_models/en/ljspeech/glow-tts'):
        self.model_name = model_name
        self.tts = TTS(self.model_name, progress_bar=False, gpu=False)

    def text_to_speech(self, text: str) -> bytes:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                wav_path = fp.name
            self.tts.tts_to_file(text=text, file_path=wav_path)
            with open(wav_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            return audio_data
        except Exception as e:
            return b""
