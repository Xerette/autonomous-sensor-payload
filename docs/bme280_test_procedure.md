# BME280 Environmental Sensor Test Procedure

## Purpose

This document describes the test procedure used to collect and analyze environmental sensor data from the SparkFun BME280 atmospheric sensor connected to a Raspberry Pi Pico W.

The goal is to evaluate basic sensor behavior, including short-term stability, drift, and response to local environmental changes.

## Hardware

* Raspberry Pi Pico W
* SparkFun BME280 Atmospheric Sensor
* Breadboard
* Jumper wires
* USB cable connected to laptop

## Software

* MicroPython firmware on Raspberry Pi Pico W
* Python laptop-side serial logging script
* Python analysis scripts using pandas and matplotlib

## Sensor Connection

The BME280 is connected to the Pico W using I2C.

| BME280 Pin | Pico W Pin | Function     |
| ---------- | ---------- | ------------ |
| GND        | GND        | Ground       |
| 3V3        | 3V3        | Sensor power |
| SDA        | GP0        | I2C data     |
| SCL        | GP1        | I2C clock    |

The sensor was detected at I2C address `0x77` / decimal `119`.

## Standard Logging Procedure

1. Confirm the BME280 is connected securely to the breadboard.
2. Confirm the Pico W is running the robust `main.py` logger firmware.
3. Close Thonny so the serial port is available.
4. Reboot the Pico W by unplugging and reconnecting the USB cable.
5. Run the laptop-side serial logging script from the project root folder.
6. Save the CSV output in `data/raw/`.
7. Run the analysis script to generate plots and summary statistics.
8. Save processed outputs in `data/processed/`.

## Baseline Stability Test

The baseline stability test is used to observe sensor behavior under normal room conditions.

Recommended duration:

```text
300 seconds
```

Command example:

```bash
python tools/capture_serial_bme280.py --port COM5 --duration 300 --output data/raw/bme280_5min_serial_log.csv
```

## Thermal/Humidity Response Test

The thermal/humidity response test is used to observe how the BME280 reacts to a local environmental disturbance.

Test segments:

| Time Range | Condition                                 |
| ---------- | ----------------------------------------- |
| 0–60 s     | Baseline room condition                   |
| 60–120 s   | Hand held near sensor without touching it |
| 120–300 s  | Recovery period                           |

Important controls:

* Do not touch the sensor.
* Do not breathe directly onto the sensor.
* Keep the hand distance as consistent as possible.
* Keep the board and breadboard still during the test.
* Record any unusual room conditions or movement.

Command example:

```bash
python tools/capture_serial_bme280.py --port COM5 --duration 300 --output data/raw/bme280_thermal_response_5min.csv
```

## Data Analysis

Each dataset should be analyzed for:

* Mean
* Standard deviation
* Minimum
* Maximum
* Drift over test duration
* Visual trends in temperature, pressure, and humidity plots

## Notes for Future Improvement

Future tests should include repeated trials, more controlled sensor placement, fixed hand distance, and longer-duration logging. Additional sensors such as an IMU can be added later to expand the payload beyond environmental sensing.
