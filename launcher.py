import sys
import os

# Ensure we can find the src module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("AI-APL Studio Launcher")
    print("----------------------")
    print("1. Web Interface (Recommended)")
    print("2. Terminal Interface")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        print("Starting Web UI...")
        from src.web_ui import demo
        demo.launch(inbrowser=True)
    elif choice == '2':
        print("Starting Terminal UI...")
        from src.ui import APLStudio
        app = APLStudio()
        app.run()
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
