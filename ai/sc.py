import socket

# We'll scan the most common 'static' range for cameras in these setups
targets = [f"172.16.1.{i}" for i in range(1, 255)]
# 8000 (Hikvision), 37777 (Dahua), 554 (RTSP Stream), 80 (Web)
camera_ports = [8000, 37777, 554, 80]

print("[*] Dashboard hung? No problem. Scanning for raw camera signatures...")

for ip in targets:
    for port in camera_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1) # Super fast for your PC
        if s.connect_ex((ip, port)) == 0:
            brand = "Unknown"
            if port == 8000: brand = "Hikvision / CP Plus"
            if port == 37777: brand = "Dahua / Lorex"
            if port == 554: brand = "Live Stream (RTSP)"
            
            print(f"[!] DETECTED: {ip} is a {brand} device (Port {port})")
        s.close()

print("[*] Finished. If an IP popped up, that's your target.")