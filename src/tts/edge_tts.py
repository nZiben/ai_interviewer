"""Edge TTS Integration"""
import tempfile
import edge_tts

class EdgeTTS:
    def __init__(self, voice='ru-RU-DmitryNeural'):
        """voice - голос для синтеза речи"""
        self.voice = voice

    def text_to_speech(self, text: str) -> bytes:
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
                output_file = fp.name
            communicate = edge_tts.Communicate(text, self.voice)
            communicate.save_sync(output_file)
            with open(output_file, 'rb') as audio_file:
                audio_data = audio_file.read()
            return audio_data
        except Exception as e:
            return b""
