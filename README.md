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

- [x] Created GitHub repository
- [x] Set up project folder structure
- [x] Created parts inventory file
- [ ] Verify all purchased components
- [ ] Complete microcontroller blink test
- [ ] Read first IMU sensor data
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

### Checkpoint 1 — Pico W Setup
- Installed MicroPython on the Raspberry Pi Pico W.
- Connected the Pico W to Thonny.
- Verified board functionality using the onboard LED blink test.
- Confirmed the development environment is ready for sensor integration.

