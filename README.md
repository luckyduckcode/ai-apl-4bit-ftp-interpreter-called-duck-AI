# AI-APL Studio

Welcome to the **AI-APL Studio**, a modern, GPU-accelerated APL interpreter designed for AI workloads. It features a VS Code-like terminal interface and runs on Python 3.12 with PyTorch support.

## 🚀 Quick Start (For Idiots & Geniuses Alike)

### 1. Install Prerequisites
You need **Python 3.12**. If you don't have it, download it from python.org.

### 2. Install Dependencies
Open your terminal (PowerShell or CMD) in this folder and run:
```bash
pip install -r requirements.txt
```
*This installs PyTorch (for AI stuff), NumPy (for math), and Textual (for the cool UI).*

### 3. Run the Studio
You have three options:

**Option A: Executable (Easiest)**
Go to `dist/AI-APL-Studio/` and run `AI-APL-Studio.exe`.
*No Python installation required for this!*

**Option B: Web Interface**
```bash
python src/web_ui.py
```

**Option C: Terminal Interface**
```bash
python src/ui.py
```

## 🎮 How to Use

Once the interface opens, you'll see:
- **Left Sidebar**: Your file explorer.
- **Top Area**: The output log (where answers appear).
- **Bottom Bar**: The input box (where you type code).

### Basic APL Commands
Type these into the input box:

| Command | Description | Example |
|---------|-------------|---------|
| `⍳N` | Generate numbers 0 to N-1 | `⍳5` -> `[0, 1, 2, 3, 4]` |
| `R C ⍴ DATA` | Reshape data into R rows, C cols | `2 3 ⍴ ⍳6` |
| `A <- ...` | Save a variable | `A <- ⍳10` |

### AI Features
This interpreter uses **PyTorch** under the hood.
- If you have an NVIDIA GPU, it automatically uses **CUDA**.
- All arrays are actually **PyTorch Tensors**.

## ⚡ Quick Test
Want to test a model without opening the UI? Use the quick run script:

```bash
# Test a preset model (tinyllama or mistral)
python scripts/quick_run.py tinyllama "Why is the sky blue?"

# Test a custom APL model definition
python scripts/quick_run.py models/demo.apl
```

## 🛠 Troubleshooting

**"Module not found" error?**
You didn't run `pip install -r requirements.txt`. Do it now!

**"CUDA not available"?**
You might not have an NVIDIA GPU or the right drivers. It will fall back to CPU automatically, so don't worry.

**"Weird characters?"**
APL uses symbols like `⍴` (rho) and `⍳` (iota). You can copy-paste them or use a special keyboard layout.
