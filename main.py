import json
import time
import machine
import hashlib
import ubinascii

# https://github.com/iot-lnu/applied-iot/tree/master/network-examples/ccs811-bmp180-dht22-MQTT
from mqtt import MQTTClient

# https://github.com/mihai-dinculescu/micropython-adafruit-drivers/tree/master/seesaw
from stemma_soil_sensor import StemmaSoilSensor

with open("config.json") as f:
    config = json.load(f)

SDA_PIN = "P23" # update this to your pin in use
SCL_PIN = "P22" # update this to your pin in use

i2c = machine.I2C(0, pins=(SDA_PIN, SCL_PIN))
seesaw = StemmaSoilSensor(i2c)

# Adafruit IO (AIO) configuration below
AIO_CLIENT_ID = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # md5 hash of WLAN mac
AIO_SERVER = config["AIO_SERVER"]
AIO_PORT = config["AIO_PORT"]
AIO_USER = config["AIO_USER"]
AIO_KEY = config["AIO_KEY"]
AIO_SOIL_MOISTURE_FEED = config["AIO_SOIL_MOISTURE_FEED"]
AIO_TEMPERATURE_FEED = config["AIO_TEMPERATURE_FEED"]

# Initialize and connect to MQTT client
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
client.connect()

while True:

    moisture = seesaw.get_moisture()
    print('moisture: ' + str(moisture))
    client.publish(AIO_SOIL_MOISTURE_FEED, str(moisture))

    temperature = seesaw.get_temp()
    print('temperature: ' + str(temperature))
    client.publish(AIO_TEMPERATURE_FEED, str(temperature))

    time.sleep(60 * 60)
