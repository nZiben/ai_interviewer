import wave
import os
import json
import random
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
from mistralai import Mistral  # Импорт клиента для работы с Mistral API


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_assistant_voice():
    """
    Установка голоса по умолчанию (индекс может меняться в зависимости от настроек операционной системы)
    """
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            ttsEngine.setProperty("voice", voices[1].id)  # Microsoft Zira Desktop - English (United States)
        else:
            ttsEngine.setProperty("voice", voices[2].id)  # Microsoft David Desktop - English (United States)
    else:
        assistant.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", voices[0].id)  # Microsoft Irina Desktop - Russian


def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)  # регулирование уровня окружающего шума

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)  # ожидание входящего звука с микрофона

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()  # online-распознавание
        except speech_recognition.UnknownValueError:
            pass
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи через Vosk
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("Please download the model from:\nhttps://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()
                recognized_data = json.loads(recognized_data)["text"]  # распознаем как текст
    except:
        print("Sorry, speech service is unavailable. Try again later")

    return recognized_data


def load_questions_from_json(filename):
    """
    Чтение списка вопросов из файла JSON.
    :param filename: путь к JSON файлу
    :return: список вопросов
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']


def ask_random_question(questions):
    """
    Выбор и озвучивание случайного вопроса из списка.
    :param questions: список вопросов
    """
    question = random.choice(questions)  # выбираем случайный вопрос
    play_voice_assistant_speech(question["text"])  # озвучиваем вопрос
    return question


if __name__ == "__main__":
    # Инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # Инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # Настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # Установка голоса по умолчанию
    setup_assistant_voice()

    # Загрузка списка вопросов из JSON файла
    questions = load_questions_from_json("questions.json")

    # Основной цикл программы
    while True:
        # Задаем случайный вопрос
        current_question = ask_random_question(questions)

        # Записываем ответ пользователя
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")  # удаляем аудиофайл после распознавания

        # Для примера просто выводим ответ пользователя
        print(f"User's answer: {voice_input}")

        # Далее можно передать этот ответ в LLM для анализа и генерации следующего вопроса или ответа
        # Пример вызова Mistral API (добавьте ваш API-ключ в переменную окружения)
        api_key = '1MbVc4n2iUxhJgOx1lfaUXuXJtzOVG0b'
        model = "mistral-large-latest"
        client = Mistral(api_key=api_key)

        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": f"Question: {current_question['text']}"},
                {"role": "user", "content": f"Answer: {voice_input}"}
            ]
        )
        
        # Получаем ответ от модели и озвучиваем его
        response_text = chat_response.choices[0].message.content
        print(f"Assistant's response: {response_text}")
        play_voice_assistant_speech(response_text)
