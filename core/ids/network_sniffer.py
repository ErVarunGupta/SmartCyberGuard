import scapy.all as scapy

sniff = scapy.sniff
IP = scapy.IP
from core.ids.feature_extractor import extract_features
from core.ids.ids_engine import predict_attack
from utils.logger import log_event

def process_packet(packet):
    if IP in packet:
        src_ip, features = extract_features(packet)

        if not features:
            return

        prediction = predict_attack(features, src_ip)
        log_event(prediction, src_ip)

def start_sniffing(interface=None):
    print("[*] Starting packet sniffing...")
    sniff(prn=process_packet, iface=interface, store=False)
