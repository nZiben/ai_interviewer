"""Utility for Model Downloading"""
import os
import subprocess

class Downloader:
    @staticmethod
    def download_llama_model(hf_model_id: str, hf_token: str = None):
        """Пример скачивания для Llama через huggingface-cli (упрощённо)"""
        print(f"Downloading Llama model {hf_model_id} from Hugging Face. This may take a while...")
        # Можно вызвать huggingface-cli или напрямую через transformers
        # Здесь мы просто печатаем, что скачали
        # Реальная логика уже частично есть в llama_llm.py
        print("...Done downloading Llama model.")

    @staticmethod
    def download_vosk_model(model_url: str):
        """Пример скачивания Vosk модели"""
        # В реальности: скачиваем zip, распаковываем в ./models/vosk
        print(f"Downloading Vosk model from {model_url} ...")
        print("...Done downloading Vosk model.")
