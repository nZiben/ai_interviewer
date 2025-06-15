"""OpenAI Whisper Integration"""
import whisper
import tempfile
import os

class WhisperSTT:
    def __init__(self, model_name='tiny'):
        """model_name может быть 'tiny', 'base', 'small', 'medium', 'large'"""
        self.model = whisper.load_model(model_name)

    def speech_to_text(self, audio_data: bytes) -> str:
        # Сохраняем байты во временный файл
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as fp:
            fp.write(audio_data)
            temp_wav_path = fp.name

        result_text = ""
        try:
            transcription = self.model.transcribe(temp_wav_path)
            result_text = transcription.get('text', '')
        except Exception as e:
            result_text = f"[Whisper Error]: {str(e)}"
        finally:
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
        return result_text
