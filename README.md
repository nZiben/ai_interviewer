# Telegram Interview Bot

## Project Description

*Telegram Interview Bot** is a job interview preparation bot that asks questions and expects answers from the user in text or voice format. The bot supports speech synthesis for questions and voice recognition for answers, which allows the user to interact with the bot through audio messages.

The project uses technologies such as python-telegram-bot to interact with the Telegram API, pyttsx3 to convert text to speech, and Vosk for offline voice recognition. The main task of the bot is to train users to successfully complete interviews.

## Features

- Asking random questions to prepare for the interview.
- Sending questions to the user in the form of a voice message and a duplicate text.
- Waiting for a response from the user in the format of a voice or text message.
- Checking the correctness of the response and providing feedback.
- A button to request a new question.

## Installation

### Requirements

- **Python** versions 3.7 and higher.
- Package manager **pip**.

### Dependencies

To install all the necessary dependencies, run the following command:

```bash
pip install python-telegram-bot pyttsx3 vosk SpeechRecognition
