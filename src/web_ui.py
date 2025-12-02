import gradio as gr
try:
    from .interpreter import APLInterpreter
except ImportError:
    from interpreter import APLInterpreter
import json

# Initialize interpreter
interp = APLInterpreter()

def execute_code(code, history):
    """Executes APL code and returns output + updated history."""
    if not code.strip():
        return "", history, None
    
    try:
        result = interp.eval(code)
        # Format result
        if hasattr(result, 'shape'):
            output = f"Tensor Shape: {result.shape}\nData:\n{result}"
        else:
            output = str(result)
            
        history.append((code, output))
        return "", history, get_structure_md()
    except Exception as e:
        history.append((code, f"Error: {str(e)}"))
        return "", history, get_structure_md()

def get_structure_md():
    """Returns markdown representation of the model structure."""
    layers = interp.get_model_structure()
    if not layers:
        return "*No model defined.*"
    
    md = "### Model Architecture\n\n"
    md += "| Layer | Name | Type | Shape | Quantization |\n"
    md += "|---|---|---|---|---|\n"
    
    for i, l in enumerate(layers):
        shape_str = "x".join(map(str, l['shape']))
        md += f"| {i} | **{l['name']}** | `{l['type']}` | {shape_str} | {l['quantization']} |\n"
        
    return md

def load_preset(model_name):
    res = interp.eval(f"LoadModel '{model_name}'")
    return res, get_structure_md()

# Custom CSS for a darker, IDE-like feel
custom_css = """
.gradio-container { background-color: #1e1e1e; }
#code-input textarea { font-family: 'Consolas', 'Monaco', monospace; }
"""

with gr.Blocks(title="AI-APL Studio") as demo:
    demo.css = custom_css
    demo.theme = gr.themes.Soft()
    gr.Markdown("# 🧠 AI-APL Studio Web Interface")
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Interpreter Session", height=500)
            code_input = gr.Textbox(
                label="APL Code Input", 
                placeholder="Type command here (e.g. Layer 'L1' 'Linear' 64)...",
                lines=3,
                elem_id="code-input"
            )
            with gr.Row():
                run_btn = gr.Button("Run Code", variant="primary")
                clear_btn = gr.Button("Clear Session")

        with gr.Column(scale=1):
            gr.Markdown("## 🏗️ Model Visualizer")
            structure_view = gr.Markdown("*No model defined.*")
            
            gr.Markdown("### Quick Actions")
            with gr.Row():
                btn_tiny = gr.Button("Load TinyLlama")
                btn_mistral = gr.Button("Load Mistral")
            
            gr.Markdown("### Assistant Tips")
            gr.Markdown("""
            - Use `Layer 'Name' 'Type' Shape` to build.
            - Use `LoadModel 'name'` for presets.
            - Use `Run 'text'` to test inference.
            """)

    # Event Handlers
    # Note: Chatbot expects list of [user, bot] messages for 'messages' type? 
    # Actually for standard Chatbot it is list of tuples.
    # Let's stick to standard list of tuples for history.
    
    # Wrapper to handle the history format for Gradio Chatbot
    def run_wrapper(code, history):
        # history is list of [msg, response]
        if history is None: history = []
        
        if not code.strip():
            return "", history, get_structure_md()
            
        try:
            result = interp.eval(code)
            output = str(result)
            history.append([code, output])
        except Exception as e:
            history.append([code, f"Error: {str(e)}"])
            
        return "", history, get_structure_md()

    run_btn.click(
        run_wrapper, 
        inputs=[code_input, chatbot], 
        outputs=[code_input, chatbot, structure_view]
    )
    
    code_input.submit(
        run_wrapper, 
        inputs=[code_input, chatbot], 
        outputs=[code_input, chatbot, structure_view]
    )
    
    clear_btn.click(lambda: None, None, chatbot, queue=False)
    
    # Preset buttons
    def preset_wrapper(name, history):
        if history is None: history = []
        res, struct = load_preset(name)
        history.append([f"LoadModel '{name}'", res])
        return history, struct

    btn_tiny.click(lambda h: preset_wrapper("tinyllama", h), inputs=[chatbot], outputs=[chatbot, structure_view])
    btn_mistral.click(lambda h: preset_wrapper("mistral", h), inputs=[chatbot], outputs=[chatbot, structure_view])

if __name__ == "__main__":
    demo.launch()
