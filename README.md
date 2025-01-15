# LLM-based Survey System with TTS and STT

This project provides a **fully working** web-based survey system utilizing multiple Large Language Models (LLM), Text-to-Speech (TTS), and Speech-to-Text (STT) technologies, as specified in the Technical Requirements. It is designed to allow **administrators** to configure models (both via private APIs and downloadable open-source models) easily using a **Streamlit admin interface**, while **end users** can participate in surveys through a friendly user interface.

## Features

- **LLM Models** (private & open-source):
  - OpenAI, Claude, Mistral, Yandex LLM, Gigachat
  - Llama (downloadable via Hugging Face, GPU/CPU usage).
- **TTS Models**:
  - Coqui TTS, Mozilla TTS, Google Cloud Text-to-Speech, Amazon Polly, ElevenLabs
- **STT Models**:
  - OpenAI Whisper, Vosk, Google Cloud Speech-to-Text, Amazon Transcribe
- **SQL Database**:
  - Stores user info, answers, feedback, and scores (SQLite by default, but configurable)
- **Streamlit-Based Interfaces**:
  - **admin_interface.py** for configuring & launching surveys
  - **user_interface.py** for end-user participation
- **One-click Download** of open-source models (Llama, Vosk) demonstrated in code
- **Random Questions** & **JSON upload** for questions
- **Scalability**: Handles parallel user sessions
- **Installable**: Organized as a Python package

## Requirements

- Python 3.8+
- GPU (optional, but recommended for heavy LLMs)
- Access to relevant API keys if using private models or TTS/STT services
- [See requirements.txt for all Python dependencies](./requirements.txt)

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

In the project root, run:
```bash
streamlit run interface/admin_interface.py
```
This opens the admin panel in your browser (usually at http://localhost:8501).

### User Interface

In another terminal, run:
```bash
streamlit run interface/user_interface.py
```
By default, it might run at http://localhost:8502. Share that URL with end users.

### Project Structure

- **src/**:
  - **llm/**: Modules for various LLM integrations
  - **tts/**: Modules for TTS integrations
  - **stt/**: Modules for STT integrations
  - **utils/**: Shared utilities (downloaders, prompt helpers)
  - **database/**: Database models and handler
  - **main.py**: Library entry point
- **interface/**:
  - **admin_interface.py**: Streamlit admin
  - **user_interface.py**: Streamlit user
- **tests/**: Unit tests
- **requirements.txt**: Python dependencies
- **setup.py**: Installation script
- **README.md**: Project documentation

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
