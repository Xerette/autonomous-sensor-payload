from machine import Pin, I2C
import time
from bme280 import BME280

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

sensor = BME280(i2c=i2c, address=0x77)

start_time = time.time()

print("time_s,temperature_C,pressure_Pa,humidity_percent")

while True:
    current_time = time.time() - start_time

    temperature_C, pressure_Pa, humidity_percent = sensor.read_compensated_data()

    print("{},{:.2f},{:.2f},{:.2f}".format(
        current_time,
        temperature_C,
        pressure_Pa,
        humidity_percent
    ))

    time.sleep(1)
