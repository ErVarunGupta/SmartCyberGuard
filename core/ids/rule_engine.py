import time
from collections import defaultdict, deque

WINDOW_SECONDS = 5
THRESHOLD = 15

IP_ACTIVITY = defaultdict(deque)
LAST_ALERT = {}

TRUSTED_PREFIXES = ("127.", "192.168.")

def is_trusted_ip(ip):
    return ip.startswith(TRUSTED_PREFIXES)

def rule_based_detection(features, src_ip):
    if is_trusted_ip(src_ip):
        return None

    now = time.time()
    q = IP_ACTIVITY[src_ip]

    q.append(now)

    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()

    if len(q) >= THRESHOLD:
        last = LAST_ALERT.get(src_ip, 0)
        if now - last > 10:
            LAST_ALERT[src_ip] = now
            return "possible_dos"

    return None
