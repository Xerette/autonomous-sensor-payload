## BMI270 IMU (Checkpoint 3A)

Wired via Qwiic cable, daisy-chained off the BME280's Qwiic port
(BME280 stays on GP0=SDA / GP1=SCL via jumper wires; IMU shares
the same I2C bus through the Qwiic chain).

I2C scan result: [104, 119]
- 104 (0x68) = BMI270 IMU
- 119 (0x77) = BME280