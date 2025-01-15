"""Streamlit Admin Interface"""
import streamlit as st
import os

from src.utils.downloader import Downloader
from src.utils.launcher import Launcher
from src.llm.openai_llm import OpenAILLM
from src.llm.claude_llm import ClaudeLLM
from src.llm.mistral_llm import MistralLLM
from src.llm.yandex_llm import YandexLLM
from src.llm.gigachat_llm import GigachatLLM
from src.llm.llama_llm import LlamaLLM

from src.tts.coqui_tts import CoquiTTS
from src.tts.mozilla_tts import MozillaTTS
from src.tts.google_tts import GoogleTTS
from src.tts.amazon_polly import AmazonPollyTTS
from src.tts.elevenlabs import ElevenLabsTTS

from src.stt.whisper_stt import WhisperSTT
from src.stt.vosk_stt import VoskSTT
from src.stt.google_stt import GoogleSTT
from src.stt.amazon_transcribe import AmazonTranscribeSTT

from src.database.db_handler import DBHandler

db_handler = DBHandler()

def admin_app():
    st.title("Admin Interface (LLM-based Survey)")
    st.write("Configure your LLM, TTS, STT, and manage questions here.")

    # 1. LLM Selection
    st.subheader("1. Choose LLM Model")
    llm_choice = st.selectbox("LLM", ["OpenAI", "Claude", "Mistral", "Yandex LLM", "Gigachat", "Llama"])

    # Dynamic inputs
    if llm_choice == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        if st.button("Test OpenAI LLM"):
            if openai_api_key:
                llm = OpenAILLM(api_key=openai_api_key)
                test_resp = llm.generate_answer("Hello from Admin Panel")
                st.write(test_resp)
            else:
                st.error("Please provide an OpenAI API key.")
    elif llm_choice == "Claude":
        claude_api_key = st.text_input("Claude API Key", type="password")
        if st.button("Test Claude LLM"):
            if claude_api_key:
                llm = ClaudeLLM(api_key=claude_api_key)
                test_resp = llm.generate_answer("Hello from Admin Panel")
                st.write(test_resp)
            else:
                st.error("Please provide a Claude API key.")
    elif llm_choice == "Mistral":
        mistral_model_id = st.text_input("HF Model ID", value="mistralai/Mistral-7B-v0.1")
        mistral_token = st.text_input("HF Token (if private)", type="password")
        if st.button("Download & Test Mistral"):
            llm = MistralLLM(hf_model_id=mistral_model_id, hf_token=mistral_token)
            st.write(llm.generate_answer("Hello from Mistral!"))
    elif llm_choice == "Yandex LLM":
        service_account_json = st.text_input("Path to Yandex Service Account JSON")
        if st.button("Test Yandex LLM"):
            llm = YandexLLM(service_account_json)
            st.write(llm.generate_answer("Hello from Yandex LLM"))
    elif llm_choice == "Gigachat":
        api_endpoint = st.text_input("Gigachat API Endpoint", value="https://api.example.com/gigachat")
        api_key = st.text_input("Gigachat API Key", type="password")
        if st.button("Test Gigachat LLM"):
            llm = GigachatLLM(api_endpoint, api_key)
            st.write(llm.generate_answer("Hello from Gigachat"))
    elif llm_choice == "Llama":
        st.write("Download or specify a local path?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download HF Llama Model"):
                Downloader.download_llama_model("decapoda-research/llama-7b-hf")
        with col2:
            local_path = st.text_input("Local Path to Llama Model", value="./models/llama")
        if st.button("Test Llama"):
            llm = LlamaLLM(local_path=local_path, download=False)
            st.write(llm.generate_answer("Hello from Llama"))

    # 2. TTS Selection
    st.subheader("2. Choose TTS Model")
    tts_choice = st.selectbox("TTS", ["Coqui TTS", "Mozilla TTS", "Google Cloud TTS", "Amazon Polly", "ElevenLabs"])
    if tts_choice == "Coqui TTS":
        st.write("Using default Coqui model.")
    elif tts_choice == "Mozilla TTS":
        st.write("Using default Mozilla TTS model.")
    elif tts_choice == "Google Cloud TTS":
        google_creds = st.text_input("Path to Google Credentials JSON")
    elif tts_choice == "Amazon Polly":
        aws_key = st.text_input("AWS Access Key ID")
        aws_secret = st.text_input("AWS Secret Access Key", type="password")
    elif tts_choice == "ElevenLabs":
        eleven_api = st.text_input("ElevenLabs API Key", type="password")

    # 3. STT Selection
    st.subheader("3. Choose STT Model")
    stt_choice = st.selectbox("STT", ["OpenAI Whisper", "Vosk", "Google Cloud STT", "Amazon Transcribe"])
    if stt_choice == "OpenAI Whisper":
        st.write("Using openai-whisper (base model).")
    elif stt_choice == "Vosk":
        st.write("Make sure Vosk model is downloaded.")
        if st.button("Download Vosk Model"):
            Downloader.download_vosk_model("https://alphacephei.com/vosk/models")
    elif stt_choice == "Google Cloud STT":
        google_stt_creds = st.text_input("Path to Google Credentials JSON")
    elif stt_choice == "Amazon Transcribe":
        aws_stt_key = st.text_input("AWS Access Key ID")
        aws_stt_secret = st.text_input("AWS Secret Access Key", type="password")

    # 4. Upload or generate questions
    st.subheader("4. Upload or Generate Questions")
    uploaded_file = st.file_uploader("Upload JSON with Questions/Answers")
    if uploaded_file:
        st.write("File uploaded. You can parse it below.")

    random_questions_num = st.number_input("Number of random questions", 1, 100, 5)
    st.write("Or generate questions by topic.")
    topic = st.text_input("Topic")
    generate_question_count = st.number_input("Number of questions to generate", 1, 100, 5)
    if st.button("Generate/Load Questions"):
        st.write("Simulating question loading or generation...")
        # Логика генерации на базе выбранной LLM
        # ...

    # 5. Start Survey
    if st.button("Start Survey"):
        st.success("Survey started! Here is the global URL: http://localhost:8502")
        st.write("(In real deployment, it would be your server’s public IP.)")

if __name__ == "__main__":
    admin_app()
