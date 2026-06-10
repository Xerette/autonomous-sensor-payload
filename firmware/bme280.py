# bme280.py
# Minimal MicroPython BME280 driver for temperature, pressure, and humidity

import time
from micropython import const

BME280_REGISTER_DIG_T1 = const(0x88)
BME280_REGISTER_DIG_H1 = const(0xA1)
BME280_REGISTER_DIG_H2 = const(0xE1)
BME280_REGISTER_CHIPID = const(0xD0)
BME280_REGISTER_CONTROL_HUM = const(0xF2)
BME280_REGISTER_CONTROL = const(0xF4)
BME280_REGISTER_CONFIG = const(0xF5)
BME280_REGISTER_DATA = const(0xF7)


class BME280:
    def __init__(self, i2c, address=0x77):
        self.i2c = i2c
        self.address = address
        self.t_fine = 0

        chip_id = self.i2c.readfrom_mem(self.address, BME280_REGISTER_CHIPID, 1)[0]
        if chip_id != 0x60:
            raise RuntimeError("BME280 not found. Chip ID: {}".format(hex(chip_id)))

        self._read_calibration()
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONTROL_HUM, bytes([0x01]))
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONTROL, bytes([0x27]))
        self.i2c.writeto_mem(self.address, BME280_REGISTER_CONFIG, bytes([0xA0]))

    def _read16_LE(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 2)
        return data[0] | (data[1] << 8)

    def _readS16_LE(self, register):
        result = self._read16_LE(register)
        if result > 32767:
            result -= 65536
        return result

    def _read8(self, register):
        return self.i2c.readfrom_mem(self.address, register, 1)[0]

    def _read_calibration(self):
        self.dig_T1 = self._read16_LE(0x88)
        self.dig_T2 = self._readS16_LE(0x8A)
        self.dig_T3 = self._readS16_LE(0x8C)

        self.dig_P1 = self._read16_LE(0x8E)
        self.dig_P2 = self._readS16_LE(0x90)
        self.dig_P3 = self._readS16_LE(0x92)
        self.dig_P4 = self._readS16_LE(0x94)
        self.dig_P5 = self._readS16_LE(0x96)
        self.dig_P6 = self._readS16_LE(0x98)
        self.dig_P7 = self._readS16_LE(0x9A)
        self.dig_P8 = self._readS16_LE(0x9C)
        self.dig_P9 = self._readS16_LE(0x9E)

        self.dig_H1 = self._read8(0xA1)
        self.dig_H2 = self._readS16_LE(0xE1)
        self.dig_H3 = self._read8(0xE3)

        e4 = self._read8(0xE4)
        e5 = self._read8(0xE5)
        e6 = self._read8(0xE6)

        self.dig_H4 = (e4 << 4) | (e5 & 0x0F)
        if self.dig_H4 > 2047:
            self.dig_H4 -= 4096

        self.dig_H5 = (e6 << 4) | (e5 >> 4)
        if self.dig_H5 > 2047:
            self.dig_H5 -= 4096

        self.dig_H6 = self._read8(0xE7)
        if self.dig_H6 > 127:
            self.dig_H6 -= 256

    def read_raw_data(self):
        data = self.i2c.readfrom_mem(self.address, BME280_REGISTER_DATA, 8)

        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        adc_h = (data[6] << 8) | data[7]

        return adc_t, adc_p, adc_h

    def read_compensated_data(self):
        adc_t, adc_p, adc_h = self.read_raw_data()

        var1 = (((adc_t >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_t >> 4) - self.dig_T1) * ((adc_t >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        temperature = ((self.t_fine * 5 + 128) >> 8) / 100

        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33

        if var1 == 0:
            pressure = 0
        else:
            p = 1048576 - adc_p
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self.dig_P8 * p) >> 19
            p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
            pressure = p / 256

        h = self.t_fine - 76800
        h = (((((adc_h << 14) - (self.dig_H4 << 20) - (self.dig_H5 * h)) + 16384) >> 15) *
             (((((((h * self.dig_H6) >> 10) * (((h * self.dig_H3) >> 11) + 32768)) >> 10) + 2097152) *
               self.dig_H2 + 8192) >> 14))
        h = h - (((((h >> 15) * (h >> 15)) >> 7) * self.dig_H1) >> 4)
        h = 0 if h < 0 else h
        h = 419430400 if h > 419430400 else h
        humidity = (h >> 12) / 1024

        return temperature, pressure, humidity
