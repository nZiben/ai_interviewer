"""Streamlit User Interface for Survey"""
import streamlit as st
from src.database.db_handler import DBHandler
from src.llm.openai_llm import OpenAILLM
from src.stt.whisper_stt import WhisperSTT
from src.tts.coqui_tts import CoquiTTS

# Подключаем остальные модели при необходимости (здесь демонстрационно)
db_handler = DBHandler()

# Для упрощения - используем OpenAI LLM, Whisper и Coqui TTS в демо
llm = OpenAILLM(api_key="")  # Подставьте API ключ
stt = WhisperSTT(model_name='base')
tts = CoquiTTS()

questions = [
    {"question": "What is your name?", "answer": ""},
    {"question": "How is the weather today?", "answer": ""},
    {"question": "Tell us about your favorite hobby?", "answer": ""}
]

def user_app():
    st.title("Welcome to the Survey!")
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {
            "first_name": "",
            "last_name": "",
            "current_question_index": 0,
            "answers": []
        }

    # Step 1: User Info
    if st.session_state["user_data"]["first_name"] == "":
        st.session_state["user_data"]["first_name"] = st.text_input("First Name", "")
    if st.session_state["user_data"]["last_name"] == "":
        st.session_state["user_data"]["last_name"] = st.text_input("Last Name", "")

    if st.button("Start Survey") and st.session_state["user_data"]["first_name"] and st.session_state["user_data"]["last_name"]:
        st.session_state["user_data"]["current_question_index"] = 0

    idx = st.session_state["user_data"]["current_question_index"]
    if isinstance(idx, int) and idx < len(questions):
        question = questions[idx]["question"]
        st.write(f"### Question {idx+1}: {question}")

        # TTS playback
        audio_data = tts.text_to_speech(question)
        if audio_data:
            st.audio(audio_data, format="audio/wav")

        # Recording logic demo
        st.write("**Record your answer** (mocked). Normally you'd have a real audio recorder.")
        if st.button("Finish Answer"):
            # Здесь берём какую-то заготовленную аудиозапись
            # В реальности вы бы захватывали микрофон и передавали байты
            fake_audio = audio_data  # just reusing the question audio as an example
            user_text = stt.speech_to_text(fake_audio)
            st.write(f"**You said**: {user_text}")

            # Save to DB
            # Генерация фидбэка и оценки
            feedback = llm.generate_answer(f"Analyze the user answer: {user_text}")
            score = 5.0  # демо-логика

            db_handler.save_survey_result(
                st.session_state["user_data"]["first_name"],
                st.session_state["user_data"]["last_name"],
                question,
                user_text,
                feedback,
                score
            )

            st.session_state["user_data"]["current_question_index"] += 1

    elif isinstance(idx, int) and idx >= len(questions):
        st.write("**Thank you for completing the survey!**")
        st.write("Here is your feedback and scores:")
        st.write("(Mocked) Summary feedback for all your answers.")
        if st.button("Take Survey Again"):
            st.session_state["user_data"]["current_question_index"] = 0

if __name__ == "__main__":
    user_app()
