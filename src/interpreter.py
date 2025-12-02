import torch
import sys
import platform
import ctypes
import os
import numpy as np

class APLInterpreter:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.variables = {}
        self.layers = [] # Track model structure
        self.backend = self._load_backend()
        
    def _load_backend(self):
        # Try to load the compiled C++ backend
        try:
            # This is a simplified loading mechanism. In a real package, 
            # you'd import the module directly after pip installing it.
            # For now, we check if a .so or .pyd exists in build/
            return None 
        except:
            return None

    def get_python_version(self):
        return sys.version.split()[0]
        
    def get_model_structure(self):
        """Returns a list of layers for visualization."""
        return self.layers

    def define_layer(self, name, type, shape):
        """Defines a layer in the AI model structure."""
        self.layers.append({
            "name": name,
            "type": type,
            "shape": shape,
            "quantization": "4-bit FPTQ" if "Quant" in type else "FP32"
        })

    def load_preset_model(self, name):
        name = name.lower()
        self.layers = [] # Clear existing
        
        if name == "tinyllama":
            self.define_layer("Embed", "Embedding", [32000, 2048])
            for i in range(22):
                self.define_layer(f"Block{i}", "TransformerBlock", [2048])
            self.define_layer("Head", "Linear", [2048, 32000])
            return "Loaded TinyLlama (1.1B) structure."
            
        elif name == "mistral":
            self.define_layer("Embed", "Embedding", [32000, 4096])
            for i in range(32):
                self.define_layer(f"Block{i}", "TransformerBlock", [4096])
            self.define_layer("Head", "Linear", [4096, 32000])
            return "Loaded Mistral (7B) structure."
            
        return f"Unknown preset: {name}. Try 'tinyllama' or 'mistral'."

    def run_inference(self, input_str):
        if not self.layers:
            return "Error: No model loaded. Use 'LoadModel' or define layers first."
        
        # Simulate inference
        # In a real implementation, this would tokenize input and run through self.layers
        return f"Running inference on '{input_str}'...\n" \
               f"Device: {self.device}\n" \
               f"Layers: {len(self.layers)}\n" \
               f"Output: [Tensor 1x32000] (Simulated logits)"

    def run_file(self, filepath):
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"
            
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    self.eval(line)
                    count += 1
        return f"Executed {count} commands from {filepath}"

    def eval(self, code: str):
        code = code.strip()
        
        if not code:
            return ""

        if code == "help":
            return """
Commands:
  help        Show this help
  exit        Exit the studio
  
APL Examples:
  2 3 ⍴ ⍳6    Create a 2x3 matrix with numbers 0-5
  A + B       Add two tensors
  
AI Building:
  Layer 'Conv1' 'Conv2d' 64 3   Define a layer
  LoadModel 'tinyllama'         Load a preset model for testing
  Run 'Hello world'             Run inference (simulated)
  Source 'path/to/file.apl'     Run commands from a file
            """
            
        # Handle Source: Source 'path'
        if code.startswith("Source"):
            parts = code.split()
            if len(parts) >= 2:
                path = parts[1].strip("'\"")
                return self.run_file(path)

        # Handle LoadModel: LoadModel 'name'
        if code.startswith("LoadModel"):
            parts = code.split()
            if len(parts) >= 2:
                name = parts[1].strip("'\"")
                return self.load_preset_model(name)

        # Handle Run: Run 'input'
        if code.startswith("Run"):
            # Extract input string
            input_str = code[3:].strip().strip("'\"")
            return self.run_inference(input_str)

        # Handle Layer Definition: Layer 'Name' 'Type' ...
        if code.startswith("Layer"):
            parts = code.split()
            if len(parts) >= 3:
                name = parts[1].strip("'\"")
                ltype = parts[2].strip("'\"")
                shape = parts[3:]
                self.define_layer(name, ltype, shape)
                return f"Layer {name} ({ltype}) added to model structure."

        # Handle assignment: A <- ...
        if "<-" in code:
            parts = code.split("<-")
            var_name = parts[0].strip()
            value_expr = parts[1].strip()
            val = self._eval_expr(value_expr)
            self.variables[var_name] = val
            return f"{var_name} assigned."
            
        return self._eval_expr(code)

    def _eval_expr(self, expr: str):
        # Handle Reshape: A ⍴ B
        # Check for ⍴ first because it might contain ⍳ on the right side
        if "⍴" in expr:
            parts = expr.split("⍴")
            shape_str = parts[0].strip()
            data_expr = parts[1].strip()
            
            # Parse shape "2 3" -> [2, 3]
            try:
                shape = [int(x) for x in shape_str.split()]
                
                # Evaluate data
                data = self._eval_expr(data_expr)
                
                # Reshape
                if isinstance(data, torch.Tensor):
                    return data.reshape(shape)
            except:
                pass # Fall through if parsing fails

        # Handle Iota: ⍳N
        if "⍳" in expr:
            # Extract number
            try:
                n = int(expr.split("⍳")[1].strip())
                return torch.arange(n, device=self.device)
            except:
                pass
            
        # Handle simple numbers
        try:
            if " " in expr:
                # Array: 1 2 3
                return torch.tensor([float(x) for x in expr.split()], device=self.device)
            return torch.tensor(float(expr), device=self.device)
        except:
            pass
            
        # Handle variables
        if expr in self.variables:
            return self.variables[expr]

        return f"Unknown expression: {expr}"
