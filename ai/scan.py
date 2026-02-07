import socket

# Common CCTV IPs for this specific subnet
targets = ["172.16.1.1", "172.16.1.108", "172.16.0.108", "172.16.1.64"]
# 80: Web, 554: Video, 8000: Hikvision
ports = [80, 554, 8000]

print("[*] Testing the most likely 'Camera Doors' on your subnet...")

for ip in targets:
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            print(f"[!] BOOM: Found something at {ip} on port {port}")
            if port == 80:
                print(f"    -> Try opening http://{ip} in your browser.")
        s.close()