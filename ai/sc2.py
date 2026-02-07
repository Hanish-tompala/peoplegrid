import socket

target = "172.16.1.1"
# Checking common 'Management' and 'Camera' ports
ports = [443, 4433, 8443, 8080, 22, 554, 8000]

print(f"[*] Probing {target} for the real management door...")

for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"[!] SUCCESS: Port {port} is OPEN.")
        if port == 443 or port == 4433:
            print(f"    -> Use: https://{target}:{port}")
    s.close()