import ollama

MODEL = "llama3.2"


def stream_chat(message: str, history: list, transcript: str, video_id: str):
    if not transcript:
        yield "⚠️ Please load a YouTube video first using the panel on the left!"
        return

    # Build messages list — system prompt first, then history, then new message
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert assistant helping users understand a YouTube video.
Video ID: {video_id}

Here is the full transcript:
<transcript>
{transcript}
</transcript>

Rules:
- Answer questions based on the transcript only
- If something isn't covered, say so honestly
- Be concise and clear"""
        }
    ]

    # Append chat history
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})

    # Append current message
    messages.append({"role": "user", "content": message})

    accumulated = ""
    for chunk in ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True,
    ):
        accumulated += chunk["message"]["content"]
        yield accumulated


