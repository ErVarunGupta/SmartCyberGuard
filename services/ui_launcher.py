import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

def launch_ui():
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            os.path.join(PROJECT_ROOT, "dashboard", "app.py"),
            "--server.headless=true",
            "--server.port=8501"
        ],
        cwd=PROJECT_ROOT
    )

if __name__ == "__main__":
    launch_ui()
