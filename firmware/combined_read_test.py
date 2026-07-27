from machine import Pin, I2C
import time
from bme280 import BME280
from micropython_bmi270 import bmi270

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

bme = BME280(i2c=i2c, address=0x77)
bmi = bmi270.BMI270(i2c)

start_time = time.time()

print("time_s,temperature_C,pressure_Pa,humidity_percent,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z")

while True:
    current_time = time.time() - start_time

    temperature_C, pressure_Pa, humidity_percent = bme.read_compensated_data()
    accx, accy, accz = bmi.acceleration
    gyrox, gyroy, gyroz = bmi.gyro

    print("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(
        current_time,
        temperature_C, pressure_Pa, humidity_percent,
        accx, accy, accz,
        gyrox, gyroy, gyroz
    ))

    time.sleep(1)