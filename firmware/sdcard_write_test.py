from machine import SPI, Pin
import sdcard, os

spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cs = Pin(5)

sd = sdcard.SDCard(spi, cs)
os.mount(sd, '/sd')

with open('/sd/test.txt', 'w') as f:
    f.write('hello from the payload\n')

with open('/sd/test.txt', 'r') as f:
    print(f.read())

print(os.listdir('/sd'))