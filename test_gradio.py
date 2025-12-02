import gradio as gr
print(f"Gradio Version: {gr.__version__}")

try:
    with gr.Blocks() as demo:
        demo.css = ".foo { color: red; }"
        demo.theme = gr.themes.Soft()
        gr.Markdown("Hello")
    print("Success setting properties")
except Exception as e:
    print(f"Failed setting properties: {e}")

