"""Audio recording component for Streamlit"""
import queue
import threading
import wave
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av

class AudioRecorder:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.recording = False
        self.audio_frames = []
        
    def audio_callback(self, frame):
        if self.recording:
            self.audio_frames.append(frame.to_ndarray())
        return frame
    
    def start_recording(self):
        self.recording = True
        self.audio_frames = []
        
    def stop_recording(self):
        self.recording = False
        if self.audio_frames:
            # Конвертируем фреймы в WAV формат
            audio_data = np.concatenate(self.audio_frames, axis=0)
            return self._save_to_wav(audio_data)
        return None
    
    def _save_to_wav(self, audio_data):
        """Сохраняет аудио данные во временный WAV файл"""
        import tempfile
        import os
        
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        # Сохраняем аудио в WAV формат
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)  # Моно
            wf.setsampwidth(2)  # 2 байта на сэмпл
            wf.setframerate(16000)  # Частота дискретизации
            wf.writeframes(audio_data.tobytes())
        
        return temp_file.name 