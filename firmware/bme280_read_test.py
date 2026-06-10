from machine import Pin, I2C
import time
from bme280 import BME280

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

sensor = BME280(i2c=i2c, address=0x77)

while True:
    temperature_C, pressure_Pa, humidity_percent = sensor.read_compensated_data()

    print("Temperature: {:.2f} C".format(temperature_C))
    print("Pressure: {:.2f} Pa".format(pressure_Pa))
    print("Humidity: {:.2f} %".format(humidity_percent))
    print("----------------------")

    time.sleep(1)
