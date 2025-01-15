import unittest
from src.stt.whisper_stt import WhisperSTT

class TestSTT(unittest.TestCase):
    def test_whisper_stt(self):
        stt = WhisperSTT(model_name='tiny')
        # Передаем заведомо некорректный audio_data
        text = stt.speech_to_text(b'')
        # Ожидаем либо пустую строку, либо ошибку
        self.assertTrue(isinstance(text, str), "STT result should be a string")

if __name__ == '__main__':
    unittest.main()
