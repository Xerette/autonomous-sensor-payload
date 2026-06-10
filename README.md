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

### In Progress

- Format BME280 readings into CSV-style output.
- Begin logging sensor data for analysis.

### Upcoming

* Add CSV logging.
* Add IMU data collection when the IMU is available.
* Analyze sensor noise, drift, calibration, and filtering.
* Create KiCad schematic.
* Run LTspice simulation.
* Write final technical report.

- [x] Created GitHub repository
- [x] Set up project folder structure
- [x] Created parts inventory file
- [x] Verify all purchased components
- [x] Complete microcontroller blink test
- [x] Read first BME sensor data
- [ ] Log sensor data to file
- [ ] Analyze sensor data using Python
- [ ] Create KiCad schematic
- [ ] Run LTspice simulation
- [ ] Write final technical report

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

## Repository Structure

```text
autonomous-sensor-payload/
├── README.md
├── bom/
│   └── parts_inventory.md
├── firmware/
├── python_analysis/
├── data/
├── figures/
├── hardware/
│   ├── kicad/
│   └── ltspice/
└── docs/
    └── progress_photos/


