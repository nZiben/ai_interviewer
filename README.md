# LLM-based Survey System with TTS and STT

This project provides a **fully working** web-based survey system utilizing multiple Large Language Models (LLM), Text-to-Speech (TTS), and Speech-to-Text (STT) technologies, as specified in the Technical Requirements. It is designed to allow **administrators** to configure models (both via private APIs and downloadable open-source models) easily using a **Streamlit admin interface**, while **end users** can participate in surveys through a friendly user interface.

## Features

- **LLM (Language Models):**
  - OpenAI, Claude, Mistral, Yandex LLM, Gigachat, Llama (via Hugging Face)
- **TTS (Text-to-Speech):**
  - Edge TTS, Google Cloud TTS, Amazon Polly, ElevenLabs, API integrations
- **STT (Speech-to-Text):**
  - Whisper, Vosk, Google Cloud Speech-to-Text, Amazon Transcribe, API integrations
- **SQL Database** (SQLite by default)
- **Streamlit Interfaces:**
  - `pages/admin_interface.py` — for administration
  - `pages/user_interface.py` — for end users
- **Flexible question generation and editing**
- **LLM-based scoring and feedback**
- **Voice and text answers**
- **Statistics and comparison of LLM vs human scores**
- **Interactive charts (Plotly)**
- **Parallel user sessions supported**

## Requirements

- Python 3.8+
- [All dependencies are listed in requirements.txt](./requirements.txt)
- Some models require API keys

## Installation

1. **Clone** the repository (or generate from the creation script).
2. Navigate to the project root directory.
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Install the package locally:
   ```bash
   pip install .
   ```
5. (Optional) You may need to download large open-source models (e.g., Llama, Vosk) before first run.

## Usage

### Admin Interface

```bash
streamlit run app.py
```
The main page will open; select "Admin Interface".

- Admin login is required (`ADMIN_PASSWORD` environment variable, default is `admin`).

### User Interface

On the main page, select "User Interface".

- The user enters their first and last name, selects a test, and takes the survey.

## Project Structure

- **src/**
  - **llm/** — LLM integrations (OpenAI, Claude, Mistral, Yandex, Llama, etc.)
  - **tts/** — TTS integrations (Edge, Google, Amazon, ElevenLabs, etc.)
  - **stt/** — STT integrations (Whisper, Vosk, Google, Amazon, etc.)
  - **utils/** — Utilities (question manager, statistics, audio, etc.)
  - **database/** — Database models and handler
  - **main.py** — Library entry point
- **pages/**
  - **admin_interface.py** — Streamlit admin interface
  - **user_interface.py** — Streamlit user interface
- **tests/** — Unit tests
- **requirements.txt** — Python dependencies
- **setup.py** — Installation script
- **README.md** — Project documentation

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
