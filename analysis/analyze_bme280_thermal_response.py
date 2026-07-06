from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = Path("data/raw/bme280_thermal_response_trial2_5min.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASELINE_END = 60
HAND_END = 120


def save_event_plot(data, y_col, ylabel, title, output_name):
    plt.figure()
    plt.plot(data["elapsed_s"], data[y_col])
    plt.axvline(BASELINE_END, linestyle="--", label="Hand near sensor")
    plt.axvline(HAND_END, linestyle="--", label="Recovery starts")
    plt.xlabel("Elapsed Time (s)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.savefig(OUTPUT_DIR / output_name, dpi=300)
    plt.close()


def segment_stats(data, column):
    baseline = data[data["elapsed_s"] < BASELINE_END][column]
    hand_near = data[(data["elapsed_s"] >= BASELINE_END) & (data["elapsed_s"] < HAND_END)][column]
    recovery = data[data["elapsed_s"] >= HAND_END][column]

    return {
        "baseline_mean": baseline.mean(),
        "hand_near_mean": hand_near.mean(),
        "recovery_mean": recovery.mean(),
        "baseline_std": baseline.std(),
        "hand_near_std": hand_near.std(),
        "recovery_std": recovery.std(),
        "overall_min": data[column].min(),
        "overall_max": data[column].max(),
        "overall_drift": data[column].iloc[-1] - data[column].iloc[0],
    }


def main():
    data = pd.read_csv(INPUT_PATH)
    data["elapsed_s"] = data["time_s"] - data["time_s"].iloc[0]

    save_event_plot(
        data,
        "temperature_C",
        "Temperature (°C)",
        "BME280 Thermal Response Test: Temperature",
        "bme280_thermal_response_temperature.png",
    )

    save_event_plot(
        data,
        "pressure_Pa",
        "Pressure (Pa)",
        "BME280 Thermal Response Test: Pressure",
        "bme280_thermal_response_pressure.png",
    )

    save_event_plot(
        data,
        "humidity_percent",
        "Humidity (%)",
        "BME280 Thermal Response Test: Humidity",
        "bme280_thermal_response_humidity.png",
    )

    stats_path = OUTPUT_DIR / "bme280_thermal_response_summary.txt"

    with open(stats_path, "w") as file:
        file.write("BME280 Thermal Response Test Summary\n")
        file.write("===================================\n\n")
        file.write(f"Input file: {INPUT_PATH}\n")
        file.write(f"Samples: {len(data)}\n")
        file.write(f"Duration: {data['elapsed_s'].iloc[-1]:.2f} seconds\n\n")
        file.write("Test segments:\n")
        file.write("0-60 s: baseline room condition\n")
        file.write("60-120 s: hand held near sensor\n")
        file.write("120-300 s: recovery\n\n")

        for column in ["temperature_C", "pressure_Pa", "humidity_percent"]:
            stats = segment_stats(data, column)

            file.write(f"{column}\n")
            file.write(f"Baseline mean: {stats['baseline_mean']:.4f}\n")
            file.write(f"Hand-near mean: {stats['hand_near_mean']:.4f}\n")
            file.write(f"Recovery mean: {stats['recovery_mean']:.4f}\n")
            file.write(f"Baseline std: {stats['baseline_std']:.4f}\n")
            file.write(f"Hand-near std: {stats['hand_near_std']:.4f}\n")
            file.write(f"Recovery std: {stats['recovery_std']:.4f}\n")
            file.write(f"Overall min: {stats['overall_min']:.4f}\n")
            file.write(f"Overall max: {stats['overall_max']:.4f}\n")
            file.write(f"Overall drift: {stats['overall_drift']:.4f}\n")
            file.write("\n")

    print("Thermal response analysis complete.")
    print("Saved plots and summary to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()