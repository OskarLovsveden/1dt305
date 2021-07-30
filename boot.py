from network import WLAN
import machine
import json

with open("config.json") as f:
    config = json.load(f)

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

for net in nets:
    if net.ssid == config["SSID"]:
        print("Network found!")
        wlan.connect(net.ssid, auth=(net.sec, config["SSID_PASS"]), timeout=5000)

        while not wlan.isconnected():
            machine.idle()

        print("WLAN connection established!")
        break
