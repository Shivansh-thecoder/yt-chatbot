# 🎬 YouTube Summarizer + Q&A Chatbot

A local AI-powered app that summarizes any YouTube video and lets you chat with it using Q&A.

## Features
- 📋 Instant AI summary of any YouTube video
- 💬 Ask questions about the video in a chat interface
- ⚡ Streaming responses in real time
- 🔒 Fully local — powered by Ollama, no API keys needed

## Tech Stack
- [Gradio](https://gradio.app) — UI
- [Ollama](https://ollama.com) + llama3.2 — local LLM
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) — transcript fetching

## Setup

1. Install [Ollama](https://ollama.com/download) and pull the model:
```bash
   ollama pull llama3.2
```

2. Clone the repo and install dependencies:
```bash
   git clone https://github.com/Shivansh-thecoder/yt-chatbot.git
   cd yt-chatbot
   pip install -r requirements.txt
```

3. Run the app:
```bash
   python main.py
```

4. Open your browser at `http://127.0.0.1:7860`

## Project Structure
```
yt-chatbot/
├── app/
│   ├── transcript.py   # extracts video ID and fetches transcript
│   ├── summarizer.py   # streams summary using Ollama
│   ├── chat.py         # streams Q&A responses using Ollama
│   └── ui.py           # Gradio layout and wiring
└── main.py             # entry point
```