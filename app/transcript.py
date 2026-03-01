import re
from youtube_transcript_api import YouTubeTranscriptApi

MAX_TRANSCRIPT_LENGTH = 20000

def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_transcript(url: str) -> tuple[str, str]:
    video_id = extract_video_id(url.strip())

    if not video_id:
        raise ValueError("Couldn't find a valid YouTube video ID. Please check your URL.")
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        transcript_list = transcript.to_raw_data()
    except Exception as e:
        raise ValueError(f"Couldn't fetch transcript: {e}\n\nMake sure the video has captions enabled.")

    full_text = " ".join(item["text"] for item in transcript_list)

    if len(full_text) > MAX_TRANSCRIPT_LENGTH:
        full_text = full_text[:MAX_TRANSCRIPT_LENGTH] + "\n\n[Transcript truncated]"
    
    return full_text, video_id