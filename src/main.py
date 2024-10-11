import wave
import os
import json
import random
import google.cloud.texttospeech as tts
import speech_recognition as sr
from mistralai import Mistral

class VoiceAssistant:
    """
    Настройки голосового ассистента, включая имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

def setup_assistant_voice():
    """
    Установка голоса по умолчанию.
    """
    # Голос будет установлен при синтезе
    pass

def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента.
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    # Подготовка текста с использованием SSML для комбинированного синтеза
    ssml_text = f"""
    <speak>
        <voice name="ru-RU-Wavenet-A">{text_to_speech.split(" ")[0]}</voice>
        <voice name="en-US-Wavenet-B">{text_to_speech.split(" ")[1]}</voice>
        <voice name="ru-RU-Wavenet-A">{' '.join(text_to_speech.split(" ")[2:])}</voice>
    </speak>
    """
    
    # Настройка клиента Google Cloud Text-to-Speech
    client = tts.TextToSpeechClient()
    
    # Настройка синтеза речи
    synthesis_input = tts.SynthesisInput(ssml=ssml_text)
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    
    # Запрос на синтез речи
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=None,  # Устанавливаем голос через SSML
        audio_config=audio_config
    )
    
    # Сохранение аудио в файл и воспроизведение
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    
    # Проигрывание аудио
    os.system("start output.mp3")  # Для Windows, для других ОС замените команду на подходящую

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио с учетом пауз.
    """
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        print("Listening...")
        audio = recognizer.listen(microphone, timeout=5, phrase_time_limit=10)
        with open("microphone-results.wav", "wb") as file:
            file.write(audio.get_wav_data())

        try:
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data

def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи через Vosk.
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
                recognized_data = json.loads(recognized_data)["text"]
    except Exception as e:
        print(f"Error during offline recognition: {e}")

    return recognized_data

def load_questions_from_json(filename):
    """
    Чтение списка вопросов из файла JSON.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def ask_random_question(questions):
    """
    Выбор и озвучивание случайного вопроса из списка.
    """
    question = random.choice(questions)
    play_voice_assistant_speech(question["text"])
    return question

if __name__ == "__main__":
    # Инициализация инструментов распознавания и ввода речи
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "male"
    assistant.speech_language = "ru"

    # Установка голоса по умолчанию
    setup_assistant_voice()

    # Загрузка списка вопросов из JSON файла
    questions = load_questions_from_json("questions.json")

    # Основной цикл программы
    while True:
        current_question = ask_random_question(questions)

        # Записываем ответ пользователя
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")

        # Для примера просто выводим ответ пользователя
        print(f"User's answer: {voice_input}")

        # Пример вызова Mistral API
        api_key = '1MbVc4n2iUxhJgOx1lfaUXuXJtzOVG0b'
        model = "mistral-small-latest"
        client = Mistral(api_key=api_key)

        prompt = f"""
        Я задал вопрос: "{current_question['text']}".
        Ответ пользователя: "{voice_input}".

        1. Оцени корректность ответа пользователя. Ответ правильный или неправильный? Если правильный, просто скажи "Ответ верный" и не предлагай уточняющих вопросов.
        2. Если ответ частично правильный или неполный, укажи, что он "частично правильный" и предложи уточняющий вопрос, чтобы пользователь мог раскрыть свою мысль более полно.
        3. Если ответ неправильный, скажи "Ответ неверный" и предложи наводящий вопрос, который поможет пользователю понять, в каком направлении двигаться для получения правильного ответа.

        Оцени ответ и предложи уточняющий или наводящий вопрос (если это необходимо).
        """

        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Answer: {voice_input}"}
            ]
        )
        
        # Получаем ответ от модели и озвучиваем его
        response_text = chat_response.choices[0].message.content
        print(f"Assistant's response: {response_text}")
        play_voice_assistant_speech(response_text)
