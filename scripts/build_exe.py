import PyInstaller.__main__
import os
import shutil

def build():
    print("Building AI-APL Studio Executable...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    PyInstaller.__main__.run([
        'launcher.py',
        '--name=AI-APL-Studio',
        '--onedir',  # Directory based build (faster startup, easier debugging)
        '--clean',
        '--collect-all=gradio',
        '--collect-all=textual',
        '--collect-all=torch',
        '--add-data=src;src',  # Include source files
        '--add-data=models;models', # Include models directory
        '--hidden-import=src.interpreter',
        '--hidden-import=src.web_ui',
        '--hidden-import=src.ui',
    ])
    
    print("\nBuild Complete!")
    print(f"Executable is located at: {os.path.abspath('dist/AI-APL-Studio/AI-APL-Studio.exe')}")

if __name__ == "__main__":
    build()
