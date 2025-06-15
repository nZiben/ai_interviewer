"""Streamlit User Interface for Survey"""
import streamlit as st
import os
import sys
from pathlib import Path
from src.database.db_handler import DBHandler
from src.llm.mistral_api_llm import MistralAPILLM
from src.stt.whisper_stt import WhisperSTT
from src.tts.edge_tts import EdgeTTS
from src.utils.audio_recorder import AudioRecorder
from src.database.models import SurveyResult
from src.utils.question_manager import QuestionManager
from src.utils.llm_evaluator import get_llm_feedback, get_llm_score
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import queue
import threading
import wave
import numpy as np
import tempfile
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

# Добавляем корневую директорию проекта в PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Подключаем остальные модели при необходимости (здесь демонстрационно)
db_handler = DBHandler()

# Используем Mistral API LLM и Edge TTS по умолчанию
llm = MistralAPILLM()  # Будет использовать MISTRAL_API_KEY из переменных окружения
stt = WhisperSTT(model_name='base')
tts = EdgeTTS()

# Инициализируем менеджер вопросов
question_manager = QuestionManager(db_handler)

def save_answer(test_name: str, question: str, answer: str, score: int, feedback: str):
    """Save single answer to database using db_handler"""
    try:
        result = SurveyResult(
            test_name=test_name,
            first_name=st.session_state.get('first_name', ''),
            last_name=st.session_state.get('last_name', ''),
            question=question,
            answer=answer,
            score=score,
            llm_score=score,
            feedback=feedback,
            timestamp=datetime.now()
        )
        if db_handler.add_survey_result(result):
            st.success("Ответ сохранен")
        else:
            st.error("Ошибка при сохранении ответа")
    except Exception as e:
        st.error(f"Ошибка при сохранении ответа: {str(e)}")

def display_summary(questions: list, answers: list, scores: list, feedback: list):
    """Display summary of survey results"""
    st.header("Результаты опроса")
    
    # Отображаем результаты в раскрывающихся окнах
    for i, (question, answer, score, feedback_text) in enumerate(zip(questions, answers, scores, feedback), 1):
        with st.expander(f"Вопрос {i}"):
            st.write(f"**Вопрос:** {question}")
            st.write(f"**Ваш ответ:** {answer}")
            st.write(f"**Оценка:** {score}/5")
            st.write(f"**Обратная связь:** {feedback_text}")
    
    # Reset session state
    for key in ['test_started', 'current_question', 'answers', 'scores', 'feedback']:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("Тест завершен!")

def main():
    st.title("AI Интервьюер")
    
    # Initialize session state
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'scores' not in st.session_state:
        st.session_state.scores = []
    if 'feedback' not in st.session_state:
        st.session_state.feedback = []
    
    # User registration
    if not st.session_state.test_started:
        st.header("Регистрация")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.first_name = st.text_input("Имя")
        with col2:
            st.session_state.last_name = st.text_input("Фамилия")
        
        # Test selection
        available_tests = question_manager.get_all_tests()
        if not available_tests:
            st.warning("Нет доступных тестов")
            return
        
        st.session_state.selected_test = st.selectbox("Выберите тест", available_tests)
        
        if st.button("Начать тест"):
            if not st.session_state.first_name or not st.session_state.last_name:
                st.warning("Пожалуйста, введите имя и фамилию")
                return
            
            st.session_state.test_started = True
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.scores = []
            st.session_state.feedback = []
            st.rerun()
    
    # Test interface
    if st.session_state.test_started:
        # Get questions for selected test
        questions = question_manager.get_questions_for_test(st.session_state.selected_test)
        
        if not questions:
            st.warning("В выбранном тесте нет вопросов")
            return
        
        # Display current question
        if st.session_state.current_question < len(questions):
            current_question = questions[st.session_state.current_question]
            
            st.subheader(f"Вопрос {st.session_state.current_question + 1} из {len(questions)}")
            st.write(current_question)
            
            # TTS для вопроса
            if st.button("🔊 Прослушать вопрос"):
                tts = EdgeTTS()
                tts.text_to_speech(current_question)
            
            # Выбор способа ответа
            response_method = st.radio(
                "Выберите способ ответа",
                ["Текстовый ввод", "Голосовой ввод"],
                index=0
            )
            
            if response_method == "Текстовый ввод":
                answer = st.text_area("Ваш ответ")
                if st.button("Отправить ответ"):
                    if answer:
                        # Оценка ответа с помощью LLM
                        llm = MistralAPILLM()
                        score = get_llm_score(current_question, answer, llm)
                        feedback = get_llm_feedback(current_question, answer, llm)
                        
                        # Сохранение ответа и оценки в session_state
                        st.session_state.answers.append(answer)
                        st.session_state.scores.append(score)
                        st.session_state.feedback.append(feedback)
                        
                        # Сохранение в базу данных
                        save_answer(
                            st.session_state.selected_test,
                            current_question,
                            answer,
                            score,
                            feedback
                        )
                        
                        # Переход к следующему вопросу
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.warning("Пожалуйста, введите ответ")
            
            else:  # Голосовой ввод
                st.write("Нажмите кнопку 'Начать запись' и говорите. Нажмите 'Остановить запись' когда закончите.")
                
                # Создаем очередь для сбора аудио фреймов
                audio_queue = queue.Queue()
                
                def audio_callback(audio_data):
                    audio_queue.put(audio_data)
                
                # Настройка WebRTC
                webrtc_ctx = webrtc_streamer(
                    key="speech-to-text",
                    mode=WebRtcMode.RECORDING,
                    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
                    media_stream_constraints={"video": False, "audio": True},
                    audio_receiver_size=1024,
                    audio_callback=audio_callback
                )
                
                if webrtc_ctx.state.playing:
                    st.write("🎤 Запись...")
                    
                    # Собираем аудио данные
                    audio_frames = []
                    while not audio_queue.empty():
                        audio_frames.append(audio_queue.get())
                    
                    if audio_frames:
                        # Сохраняем аудио во временный файл
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                            # Создаем WAV файл с правильными параметрами
                            with wave.open(temp_audio.name, 'wb') as wf:
                                wf.setnchannels(1)  # mono
                                wf.setsampwidth(2)  # 2 bytes per sample
                                wf.setframerate(16000)  # 16kHz
                                for frame in audio_frames:
                                    wf.writeframes(frame)
                            
                            # Распознаем речь
                            stt = WhisperSTT()
                            answer = stt.transcribe(temp_audio.name)
                            
                            if answer:
                                st.write("Распознанный ответ:", answer)
                                
                                # Оценка ответа с помощью LLM
                                llm = MistralAPILLM()
                                score = get_llm_score(current_question, answer, llm)
                                feedback = get_llm_feedback(current_question, answer, llm)
                                
                                # Сохранение ответа и оценки в session_state
                                st.session_state.answers.append(answer)
                                st.session_state.scores.append(score)
                                st.session_state.feedback.append(feedback)
                                
                                # Сохранение в базу данных
                                save_answer(
                                    st.session_state.selected_test,
                                    current_question,
                                    answer,
                                    score,
                                    feedback
                                )
                                
                                # Переход к следующему вопросу
                                st.session_state.current_question += 1
                                st.rerun()
                            else:
                                st.warning("Не удалось распознать речь. Пожалуйста, попробуйте еще раз.")
                        
                        # Удаляем временный файл
                        os.unlink(temp_audio.name)
        
        # Display summary when all questions are answered
        if st.session_state.current_question >= len(questions):
            display_summary(
                questions,
                st.session_state.answers,
                st.session_state.scores,
                st.session_state.feedback
            )

if __name__ == "__main__":
    main()
