import pystray
from pystray import MenuItem as item
from PIL import Image
import subprocess
import os
import time
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def open_dashboard():
    subprocess.Popen([os.path.join(BASE_DIR, "ui_launcher.exe")])
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

def exit_app(icon, item):
    icon.stop()

icon = pystray.Icon(
    "SmartCyberGuard",
    Image.new("RGB", (64, 64), "blue"),
    "SmartCyberGuard",
    menu=(
        item("📊 Open Dashboard", open_dashboard),
        item("❌ Exit", exit_app),
    )
)

icon.run()
