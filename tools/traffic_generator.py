from scapy.all import IP, ICMP, send

target_ip = "10.159.184.80"  # your system IP

print("[*] Generating ICMP DoS burst...")

for _ in range(50):
    pkt = IP(dst=target_ip)/ICMP()
    send(pkt, verbose=False)

print("[*] Done")
