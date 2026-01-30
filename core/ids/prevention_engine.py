import subprocess
import time

BLOCKED_IPS = {}
BLOCK_DURATION = 60  # seconds

def block_ip(ip):
    if ip in BLOCKED_IPS:
        return

    print(f"[IPS] Blocking IP: {ip}")

    cmd = f'netsh advfirewall firewall add rule name="CyberGuard_Block_{ip}" dir=in action=block remoteip={ip}'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    BLOCKED_IPS[ip] = time.time()

def unblock_expired_ips():
    now = time.time()

    for ip, ts in list(BLOCKED_IPS.items()):
        if now - ts > BLOCK_DURATION:
            print(f"[IPS] Unblocking IP: {ip}")
            cmd = f'netsh advfirewall firewall delete rule name="CyberGuard_Block_{ip}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            del BLOCKED_IPS[ip]
