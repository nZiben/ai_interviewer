"""Vosk STT Integration"""
import vosk
import tempfile
import json
import os

class VoskSTT:
    def __init__(self, model_path='models/vosk'):
        """model_path - путь к распакованной модели Vosk"""
        if not os.path.exists(model_path):
            os.makedirs(model_path, exist_ok=True)
            # Здесь можно реализовать скачивание модели Vosk
            # например, wget + unzip
            # Для демонстрации оставим так
        self.model = vosk.Model(model_path)

    def speech_to_text(self, audio_data: bytes) -> str:
        import wave
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            fp.write(audio_data)
            temp_wav_path = fp.name

        rec_text = ""
        try:
            wf = wave.open(temp_wav_path, "rb")
            rec = vosk.KaldiRecognizer(self.model, wf.getframerate())
            data = wf.readframes(4000)
            while len(data) > 0:
                if rec.AcceptWaveform(data):
                    pass
                data = wf.readframes(4000)
            final = rec.FinalResult()
            rec_json = json.loads(final)
            rec_text = rec_json.get("text", "")
            wf.close()
        except Exception as e:
            rec_text = f"[Vosk Error]: {str(e)}"
        finally:
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
        return rec_text
