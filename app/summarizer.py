import ollama

MODEL = "llama3.2"


def stream_summary(transcript: str, video_id: str):
    prompt = f"""You are a helpful assistant that summarizes YouTube videos.

Here is the transcript:
<transcript>
{transcript}
</transcript>

Please provide a clear, well-structured summary with these sections:
1. 🎯 **Main Topic** — What is this video about? (1-2 sentences)
2. 📌 **Key Points** — The most important ideas (bullet list)
3. 💡 **Insights & Takeaways** — What the viewer should remember
4. 🏷️ **Tags** — 5 relevant topic tags
"""

    accumulated = ""
    for chunk in ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        accumulated += chunk["message"]["content"]
        yield accumulated