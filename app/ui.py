import gradio as gr
from app.transcript import fetch_transcript
from app.summarizer import stream_summary
from app.chat import stream_chat


def load_and_summarize(url: str):

    if not url.strip():
        yield " Please paste a YouTube URL first.", "", ""
        return

    # Step 1 — show a loading message while fetching transcript
    yield " Fetching transcript...", "", ""

    try:
        transcript, video_id = fetch_transcript(url)
    except ValueError as e:
        yield str(e), "", ""
        return

    yield f" Transcript fetched — generating summary...", transcript, video_id

    # Step 2 — stream the summary, updating the UI on every chunk
    # We keep passing transcript and video_id through so gr.State stays updated
    for partial_summary in stream_summary(transcript, video_id):
        yield partial_summary, transcript, video_id


def build_ui():
    """
    Builds and returns the Gradio Blocks app.
    We define it in a function so main.py stays clean — it just calls build_ui().

    gr.Blocks() gives us full layout control via gr.Row() and gr.Column().
    Think of Row as a horizontal flexbox and Column as a vertical one.
    scale= controls how much space each column takes (like flex-grow).
    """

    with gr.Blocks(
        title="YouTube Summarizer + Q&A",
    ) as app:

        # ── Header ──
        gr.Markdown("""
        #  YouTube Summarizer + Q&A
        Paste a YouTube URL to get an AI summary, then ask questions about the video.
        """)

        # ── URL Input Row ──
        with gr.Row():
            url_input = gr.Textbox(
                label="YouTube URL",
                placeholder="https://www.youtube.com/watch?v=...",
                scale=5,
            )
            summarize_btn = gr.Button(" Summarize", variant="primary", scale=1)

        # ── gr.State: invisible variables that persist across interactions ──
        # These are NOT shown in the UI but can be passed into and out of functions.
        # transcript_state holds the raw text, video_id_state holds the ID.
        # Both get updated when summarize_btn is clicked and read by stream_chat.
        transcript_state = gr.State("")
        video_id_state = gr.State("")

        # ── Side-by-side Layout ──
        with gr.Row(equal_height=True):

            # LEFT: Summary panel
            with gr.Column(scale=1):
                gr.Markdown("##  Summary")
                summary_output = gr.Markdown(
                    value="*Your summary will appear here after loading a video.*"
                )

            # RIGHT: Chat panel
            with gr.Column(scale=1):
                gr.Markdown("## Ask Questions")
                gr.ChatInterface(
                    fn=stream_chat,
                    # additional_inputs passes gr.State values into stream_chat
                    # They map positionally to the extra params: transcript, video_id
                    additional_inputs=[transcript_state, video_id_state],
                    chatbot=gr.Chatbot(
                        placeholder="<b>Load a video first, then ask anything!</b>",
                        height=500,
                    ),
                    textbox=gr.Textbox(
                        placeholder="Ask something about the video...",
                        container=False,
                        submit_btn="Send ",
                    ),
                )

        gr.Markdown("---\n **Try asking:** *'What are the main points?'* or *'Give me a quiz question about this'*")

        # ── Wire up the Summarize button ──
        # inputs:  what to read from the UI
        # outputs: what to write back to the UI (must match yield order in load_and_summarize)
        summarize_btn.click(
            fn=load_and_summarize,
            inputs=[url_input],
            outputs=[summary_output, transcript_state, video_id_state],
        )

        # Also fire on Enter key in the URL box
        url_input.submit(
            fn=load_and_summarize,
            inputs=[url_input],
            outputs=[summary_output, transcript_state, video_id_state],
        )

    return app