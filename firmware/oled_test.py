from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
print(i2c.scan())  # sanity check — should now show 3 addresses

oled = SSD1306_I2C(128, 64, i2c, addr=0x3d)

oled.fill(0)
oled.text("Sensor Payload", 0, 0)
oled.text("Online", 0, 20)
oled.show()