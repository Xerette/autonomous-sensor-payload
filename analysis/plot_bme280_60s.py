import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_path = Path("data/raw/bme280_60s_test.csv")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

data = pd.read_csv(data_path)

plt.figure()
plt.plot(data["time_s"], data["temperature_C"])
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("BME280 Temperature vs Time")
plt.grid(True)
plt.savefig(output_dir / "bme280_temperature_60s.png", dpi=300)
plt.show()

plt.figure()
plt.plot(data["time_s"], data["pressure_Pa"])
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.title("BME280 Pressure vs Time")
plt.grid(True)
plt.savefig(output_dir / "bme280_pressure_60s.png", dpi=300)
plt.show()

plt.figure()
plt.plot(data["time_s"], data["humidity_percent"])
plt.xlabel("Time (s)")
plt.ylabel("Humidity (%)")
plt.title("BME280 Humidity vs Time")
plt.grid(True)
plt.savefig(output_dir / "bme280_humidity_60s.png", dpi=300)
plt.show()