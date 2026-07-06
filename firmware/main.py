from machine import Pin, I2C
import time
from bme280 import BME280

# Onboard LED for status indication
led = Pin("LED", Pin.OUT)

# I2C setup
# Reduced frequency improves reliability with breadboard jumper wiring
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=50000)

sensor = BME280(i2c=i2c, address=0x77)

start_time = time.time()

print("time_s,temperature_C,pressure_Pa,humidity_percent")

while True:
    current_time = time.time() - start_time

    try:
        temperature_C, pressure_Pa, humidity_percent = sensor.read_compensated_data()

        print("{},{:.2f},{:.2f},{:.2f}".format(
            current_time,
            temperature_C,
            pressure_Pa,
            humidity_percent
        ))

        # Short LED blink = successful reading
        led.on()
        time.sleep(0.05)
        led.off()

    except OSError as error:
        # Do not crash if one I2C read fails
        # The laptop logger ignores this because it is not a 4-column CSV row
        print("#ERROR,I2C read failed,{}".format(error))

        # Longer LED blink = sensor read error
        led.on()
        time.sleep(0.3)
        led.off()

    time.sleep(1)