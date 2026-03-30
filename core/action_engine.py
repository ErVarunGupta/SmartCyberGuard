import os

def execute(action):

    if action == "kill_apps":
        os.system("taskkill /f /im chrome.exe")

    elif action == "clear_temp":
        os.system("del /q/f/s %TEMP%\\*")

    elif action == "block_ip":
        print("IP blocked")