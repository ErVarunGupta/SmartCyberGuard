# tools/traffic_generator.py
import socket
import time
import random

TARGET = ("8.8.8.8", 80)

print("[*] Generating IDS test traffic...")

for i in range(50):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(TARGET)
        s.send(b"GET / HTTP/1.1\r\n\r\n")
        s.close()
    except:
        pass

    time.sleep(random.uniform(0.05, 0.2))

print("[+] Traffic generation finished")
