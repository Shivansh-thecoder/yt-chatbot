from app.ui import build_ui

if __name__ == "__main__":
    import gradio as gr
    app = build_ui()
    app.launch(
        share=True,
        show_error=True,  # show full error tracebacks in the UI during development
        theme=gr.themes.Soft(),
    )