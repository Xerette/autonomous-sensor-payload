from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

devices = i2c.scan()

print("I2C devices found:", devices)

if len(devices) == 0:
    print("No I2C devices detected.")
else:
    for device in devices:
        print("Device address:", device, "hex:", hex(device))
