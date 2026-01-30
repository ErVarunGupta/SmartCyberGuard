import sys
import os

# 🔥 ADD PROJECT ROOT (parent of cyber_guard)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from scapy.all import sniff
from engine.ids_engine import process_packet

print("[*] Cyber-Guard IDPS started")
print("[*] Sniffing packets...")

sniff(prn=process_packet, store=False)
