from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Log, Static, Button, Tree, TabbedContent, TabPane
from textual.widgets.tree import Tree
try:
    from .interpreter import APLInterpreter
except ImportError:
    from src.interpreter import APLInterpreter
import os
import random

class FileTree(Tree):
    def on_mount(self):
        self.root.expand()
        
    def load_directory(self, path: str):
        self.clear()
        self.root.label = os.path.basename(path) or path
        self.root.data = path
        self._add_children(self.root, path)
        
    def _add_children(self, node, path):
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    if not entry.name.startswith('.'):
                        child = node.add(entry.name, expand=False, data=entry.path)
                        child.allow_expand = True
                        # Lazy loading could go here
                        self._add_children(child, entry.path)
                else:
                    node.add_leaf(entry.name, data=entry.path)
        except PermissionError:
            pass

class ModelVisualizer(Static):
    """Visualizes the AI model structure."""
    
    def update_structure(self, layers):
        self.update("") # Clear
        if not layers:
            self.update("[italic dim]No model layers defined yet.[/]")
            return
            
        output = "[bold underline]Current AI Model Structure:[/]\n\n"
        for i, layer in enumerate(layers):
            output += f"[bold cyan]Layer {i+1}: {layer['name']}[/]\n"
            output += f"  Type: [green]{layer['type']}[/]\n"
            output += f"  Shape: {layer['shape']}\n"
            output += f"  Quant: [yellow]{layer['quantization']}[/]\n"
            output += "  [dim]↓[/]\n"
        
        output += "[bold]Output[/]"
        self.update(output)

class AIAssistant(Static):
    """Provides suggestions and help."""
    
    SUGGESTIONS = [
        "Try defining a layer: Layer 'L1' 'Linear' 128 64",
        "Use ⍳N to generate a range.",
        "Remember: APL evaluates from right to left!",
        "Assign variables with <-"
    ]
    
    def on_mount(self):
        self.update_suggestion()
        
    def update_suggestion(self):
        sugg = random.choice(self.SUGGESTIONS)
        self.update(f"[bold magenta]AI Assistant Tip:[/]\n{sugg}")

class APLStudio(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 20% 80%;
    }

    #sidebar {
        dock: left;
        width: 100%;
        height: 100%;
        background: $panel;
        border-right: vkey $accent;
    }

    #main-area {
        height: 100%;
        width: 100%;
        layout: vertical;
    }

    #output-log {
        height: 1fr;
        background: $surface;
        border: solid $accent;
        color: $text;
    }
    
    #viz-area {
        height: 1fr;
        background: $surface;
        border: solid $accent;
        padding: 1;
    }

    #input-area {
        height: auto;
        dock: bottom;
        padding: 1;
        background: $panel;
    }

    Input {
        dock: bottom;
        width: 100%;
        border: tall $accent;
    }
    
    .title {
        content-align: center middle;
        text-style: bold;
        background: $primary;
        color: $text;
        height: 3;
    }
    """

    TITLE = "AI-APL Studio"
    SUB_TITLE = "Powered by PyTorch & CUDA | 4-bit FPTQ Ready"

    def __init__(self):
        super().__init__()
        self.interpreter = APLInterpreter()

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(id="sidebar"):
            yield Static("EXPLORER", classes="title")
            yield FileTree("Root")
            yield Static("ASSISTANT", classes="title")
            yield AIAssistant()

        with Container(id="main-area"):
            with TabbedContent():
                with TabPane("Console", id="console-tab"):
                    yield Log(id="output-log", highlight=True, markup=True)
                with TabPane("Model Visualizer", id="viz-tab"):
                    yield ModelVisualizer(id="viz-area")
            
            with Container(id="input-area"):
                yield Input(placeholder="Type APL code here... (e.g. Layer 'L1' 'Linear' 64)", id="apl-input")
        
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(FileTree).load_directory(os.getcwd())
        self.query_one(Log).write("[bold green]Welcome to AI-APL Studio![/]")
        self.query_one(Log).write(f"Python: {self.interpreter.get_python_version()}")
        self.query_one(Log).write(f"Device: [bold yellow]{self.interpreter.device}[/]")
        self.query_one(Log).write("Type 'help' for commands.\n")
        self.query_one(ModelVisualizer).update_structure(self.interpreter.get_model_structure())

    def on_input_submitted(self, message: Input.Submitted) -> None:
        code = message.value
        if not code:
            return
            
        log = self.query_one(Log)
        log.write(f"[bold blue]>[/] {code}")
        
        try:
            result = self.interpreter.eval(code)
            log.write(f"[bold white]{result}[/]\n")
            
            # Update visualizer if structure changed
            self.query_one(ModelVisualizer).update_structure(self.interpreter.get_model_structure())
            
            # Update assistant
            self.query_one(AIAssistant).update_suggestion()
            
        except Exception as e:
            log.write(f"[bold red]Error: {e}[/]\n")
            
        message.input.value = ""

if __name__ == "__main__":
    app = APLStudio()
    app.run()
