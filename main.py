import json
import time
import machine
import hashlib
import ubinascii

# https://github.com/iot-lnu/applied-iot/tree/master/network-examples/ccs811-bmp180-dht22-MQTT
from mqtt import MQTTClient

# https://github.com/mihai-dinculescu/micropython-adafruit-drivers/tree/master/seesaw
from stemma_soil_sensor import StemmaSoilSensor

# Define pins for the sensor
SDA_PIN = "P23"
SCL_PIN = "P22"

# Create and use PIN assignments defined above
i2c = machine.I2C(0, pins=(SDA_PIN, SCL_PIN))
seesaw = StemmaSoilSensor(i2c)

# Adafruit IO (AIO) configuration below
AIO_CLIENT_ID = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # md5 hash of WLAN mac
AIO_SERVER = config.AIO_SERVER
AIO_PORT = config.AIO_PORT
AIO_USER = config.AIO_USER
AIO_KEY = config.AIO_KEY
AIO_SOIL_MOISTURE_FEED = config.AIO_SOIL_MOISTURE_FEED
AIO_TEMPERATURE_FEED = config.AIO_TEMPERATURE_FEED

# Initialize and connect to MQTT client
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
client.connect()

# Perferm readings "infinitely"
while True:

    # Get soil moisture and ambient temperature values
    moisture = seesaw.get_moisture()
    temperature = seesaw.get_temp()

    # Print in REPL (development)
    print('moisture: ' + str(moisture))
    print('temperature: ' + str(temperature))

    # Publish the soil moisture and ambient temperature to adafruit.io
    client.publish(AIO_SOIL_MOISTURE_FEED, str(moisture))
    client.publish(AIO_TEMPERATURE_FEED, str(temperature))

    # Wait/sleep 60s
    time.sleep(60)
