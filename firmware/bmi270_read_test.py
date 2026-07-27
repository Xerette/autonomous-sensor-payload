from machine import Pin, I2C
from micropython_bmi270 import bmi270
import time

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
bmi = bmi270.BMI270(i2c)

while True:
    accx, accy, accz = bmi.acceleration
    gyrox, gyroy, gyroz = bmi.gyro
    print("accel: x={:.2f} y={:.2f} z={:.2f} m/s2 | gyro: x={:.2f} y={:.2f} z={:.2f} deg/s".format(
        accx, accy, accz, gyrox, gyroy, gyroz))
    time.sleep(0.5) 