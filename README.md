# Autonomous Sensor Payload and Data Acquisition Test Bench

## Project Overview

This project is an independent engineering build focused on designing, prototyping, and testing a small autonomous sensor payload for data acquisition and sensor-health monitoring.

The system uses microcontroller-based sensor logging, IMU/environmental sensing, voltage/current monitoring, circuit design, and Python-based data analysis to simulate the workflow of an engineering test bench used in robotics, aerospace, embedded systems, and instrumentation applications.

## Project Goals

- Build a working sensor payload using a microcontroller and multiple sensors.
- Collect and store real sensor data.
- Analyze sensor noise, drift, calibration, and filtering using Python.
- Design supporting circuitry using KiCad and LTspice.
- Document the engineering process through test procedures, plots, and technical reports.

## Current Status

### Completed

* Created GitHub repository and initial project structure.
* Installed MicroPython on the Raspberry Pi Pico W.
* Verified Pico W functionality using the onboard LED blink test.
* Soldered male header pins onto the Pico W for breadboard prototyping.
* Confirmed Pico W functionality after soldering by repeating the onboard LED blink test.
* Wired the SparkFun BME280 atmospheric sensor to the Pico W using I2C.
* Detected the BME280 successfully at I2C address `0x77` / decimal `119`.
* Successfully read temperature, pressure, and humidity data from the BME280 sensor.
* Verified environmental sensor data output through Thonny using MicroPython.
* Streamed BME280 temperature, pressure, and humidity readings in CSV format for easier data logging and analysis.
* Captured a 60-second BME280 environmental sensor dataset in CSV format.
* Generated Python plots for BME280 temperature, pressure, and humidity over time.
* Calculated basic summary statistics for the 60-second BME280 dataset, including mean, standard deviation, minimum, maximum, and drift.
* Interpreted initial BME280 sensor stability using generated plots and summary statistics.

### In Progress

* Improve the sensor data logging workflow so CSV files can be captured more cleanly.
* Prepare the project for longer-duration environmental sensor tests.
* Add clearer documentation for test procedures and results.

### Upcoming

* Capture a longer BME280 dataset, such as 5 minutes instead of 60 seconds.
* Add automated serial-to-CSV logging from the Pico W to the laptop.
* Add IMU data collection when the IMU is available.
* Analyze sensor noise, drift, calibration, and filtering over longer test periods.
* Add wiring diagrams and hardware photos.
* Create KiCad schematic.
* Run LTspice simulation.
* Write final technical report.



## Tools and Skills

- Embedded systems
- Sensor data acquisition
- Circuit design
- KiCad
- LTspice
- Python
- Data analysis
- Technical documentation
- Git/GitHub

## Initial Results

The first environmental sensing milestone was completed using a Raspberry Pi Pico W and SparkFun BME280 atmospheric sensor.

A 60-second dataset was collected for:
- Temperature
- Pressure
- Humidity

The sensor was connected over I2C and detected at address `0x77` / decimal `119`.

Python analysis scripts were used to:
- Generate temperature, pressure, and humidity plots
- Calculate mean, standard deviation, minimum, maximum, and drift over the test period

Generated outputs are stored in:

```text
data/processed/
```
### BME280 60-Second Test Interpretation

The initial 60-second BME280 test showed stable environmental sensing performance from the Raspberry Pi Pico W and SparkFun BME280 setup.

Temperature readings remained highly stable around room temperature, with only small variation over the test period. The measured temperature had a mean of 23.3603°C and a standard deviation of 0.0146°C, indicating very low short-term noise during the test.

Pressure readings also remained stable. Although the pressure plot appears visually noisy because the y-axis is zoomed in, the measured variation was small relative to the atmospheric pressure value. The pressure data had a mean of 101614.4647 Pa and a standard deviation of 3.7636 Pa.

Humidity showed the largest variation during the test. The humidity readings ranged from 38.04% to 42.83%, with a standard deviation of 1.5495%. This may be due to local airflow, nearby hand/body heat, breathing near the sensor, or short-term environmental changes around the test setup.

Overall, this test confirms that the Pico W can reliably collect BME280 environmental data over I2C and that the first data acquisition, plotting, and summary-statistics workflow is functioning correctly.

### BME280 5-Minute Automated Logging Test

A longer 5-minute BME280 dataset was captured using the automated serial-to-CSV logging workflow. This test collected 300 samples over 300 seconds from the Raspberry Pi Pico W and SparkFun BME280 sensor.

The temperature data had a mean of 28.8979°C with a standard deviation of 0.1679°C. The temperature decreased by 0.3900°C over the test, suggesting a small thermal drift or local environmental change during the run.

The pressure data remained highly stable, with a mean of 101769.6811 Pa and a standard deviation of 3.9603 Pa. Compared with the total atmospheric pressure value, this variation is very small, indicating stable pressure measurement behavior during the test.

The humidity data had a mean of 40.4098% and a standard deviation of 0.6821%. Humidity drifted upward by 0.6600% over the 5-minute test. Compared with the earlier 60-second test, the 5-minute humidity readings showed more stable behavior overall.

This checkpoint improved the project workflow by replacing manual Thonny copy/paste logging with an automated laptop-side serial capture script. The system can now collect longer datasets more reliably and process them with reusable Python analysis tools.

