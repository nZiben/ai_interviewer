import unittest
from src.tts.coqui_tts import CoquiTTS

class TestTTS(unittest.TestCase):
    def test_coqui_tts(self):
        tts = CoquiTTS()
        audio_data = tts.text_to_speech("Hello, this is a test.")
        self.assertIsInstance(audio_data, bytes, "TTS output should be bytes")

if __name__ == '__main__':
    unittest.main()
