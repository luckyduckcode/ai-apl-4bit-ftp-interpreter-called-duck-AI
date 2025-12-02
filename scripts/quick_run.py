import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.interpreter import APLInterpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_run.py <model_name_or_file> [input_text]")
        print("Examples:")
        print("  python quick_run.py tinyllama")
        print("  python quick_run.py models/demo.apl")
        return

    target = sys.argv[1]
    input_text = sys.argv[2] if len(sys.argv) > 2 else "Hello AI"
    
    interp = APLInterpreter()
    print(f"Initializing AI-APL Interpreter on {interp.device}...")
    
    if target.endswith(".apl"):
        print(f"Executing source file: {target}")
        res = interp.eval(f"Source '{target}'")
        print(res)
    else:
        print(f"Loading preset model: {target}")
        res = interp.eval(f"LoadModel '{target}'")
        print(res)
        
    print("-" * 40)
    print(f"Running inference with input: '{input_text}'")
    res = interp.eval(f"Run '{input_text}'")
    print(res)
    print("-" * 40)
    
    # Print structure summary
    print(f"Model Structure ({len(interp.layers)} layers):")
    for l in interp.layers[:5]:
        print(f" - {l['name']} ({l['type']})")
    if len(interp.layers) > 5:
        print(f" ... and {len(interp.layers)-5} more")

if __name__ == "__main__":
    main()
