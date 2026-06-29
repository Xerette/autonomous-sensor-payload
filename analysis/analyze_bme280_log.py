import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def save_plot(data, x_col, y_col, ylabel, title, output_path):
    plt.figure()
    plt.plot(data[x_col], data[y_col])
    plt.xlabel("Elapsed Time (s)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Analyze BME280 CSV sensor logs.")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--tag", default="bme280_log", help="Output filename tag")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(input_path)

    # Normalize time so plots start at 0 seconds even if Pico had been running already
    data["elapsed_s"] = data["time_s"] - data["time_s"].iloc[0]

    plot_specs = [
        ("temperature_C", "Temperature (°C)", "BME280 Temperature vs Time", f"{args.tag}_temperature.png"),
        ("pressure_Pa", "Pressure (Pa)", "BME280 Pressure vs Time", f"{args.tag}_pressure.png"),
        ("humidity_percent", "Humidity (%)", "BME280 Humidity vs Time", f"{args.tag}_humidity.png"),
    ]

    for column, ylabel, title, filename in plot_specs:
        save_plot(
            data=data,
            x_col="elapsed_s",
            y_col=column,
            ylabel=ylabel,
            title=title,
            output_path=output_dir / filename,
        )

    stats_path = output_dir / f"{args.tag}_summary_stats.txt"

    columns = ["temperature_C", "pressure_Pa", "humidity_percent"]

    with open(stats_path, "w") as file:
        file.write("BME280 Sensor Data Summary\n")
        file.write("==========================\n\n")
        file.write(f"Input file: {input_path}\n")
        file.write(f"Samples: {len(data)}\n")
        file.write(f"Duration: {data['elapsed_s'].iloc[-1]:.2f} seconds\n\n")

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

    print("Analysis complete.")
    print("Plots and summary saved to:", output_dir)


if __name__ == "__main__":
    main()