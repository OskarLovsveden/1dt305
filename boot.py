from network import WLAN
import machine
import json

# Open and read from config.json
with open("config.json") as f:
    config = json.load(f)

# Setup as station and scan for networks
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

# Loop networks found and search for match in config SSID
for net in nets:
    if net.ssid == config["SSID"]:
        
        # Connect when match is found
        print("Network found!")
        wlan.connect(net.ssid, auth=(net.sec, config["SSID_PASS"]), timeout=5000)

        # Wait/sleep while searching for match
        while not wlan.isconnected():
            machine.idle()

        print("WLAN connection established!")
        break
