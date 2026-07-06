# BME280 Wiring Notes

## Hardware Used

- Raspberry Pi Pico W
- SparkFun BME280 Atmospheric Sensor
- Breadboard
- Jumper wires
- USB cable for power and serial communication

## Communication Protocol

The BME280 is connected to the Raspberry Pi Pico W using I2C communication.

## Wiring Table

| BME280 Pin | Raspberry Pi Pico W Pin | Purpose |
|---|---|---|
| GND | GND | Common ground |
| 3V3 | 3V3 | Sensor power |
| SDA | GP0 | I2C data |
| SCL | GP1 | I2C clock |

## I2C Address

The BME280 was detected at:

```text
0x77 / decimal 119