import pandas as pd
from pathlib import Path

data_path = Path("data/raw/bme280_60s_test.csv")
output_path = Path("data/processed/bme280_summary_stats.txt")

data = pd.read_csv(data_path)

columns = ["temperature_C", "pressure_Pa", "humidity_percent"]

with open(output_path, "w") as file:
    file.write("BME280 60-Second Sensor Data Summary\n")
    file.write("====================================\n\n")

    for column in columns:
        mean_value = data[column].mean()
        std_value = data[column].std()
        min_value = data[column].min()
        max_value = data[column].max()
        drift_value = data[column].iloc[-1] - data[column].iloc[0]

        file.write(f"{column}\n")
        file.write(f"Mean: {mean_value:.4f}\n")
        file.write(f"Standard deviation: {std_value:.4f}\n")
        file.write(f"Minimum: {min_value:.4f}\n")
        file.write(f"Maximum: {max_value:.4f}\n")
        file.write(f"Drift over test: {drift_value:.4f}\n")
        file.write("\n")

print("Summary statistics saved to:", output_path)