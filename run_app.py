import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    app_path = os.path.join("dashboard", "analyzer_app.py")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        "--server.port=8501"
    ]

    subprocess.Popen(cmd)

if __name__ == "__main__":
    main()

