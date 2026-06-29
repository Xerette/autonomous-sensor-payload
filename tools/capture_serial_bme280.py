import argparse
import csv
import time
from pathlib import Path

import serial


HEADER = ["time_s", "temperature_C", "pressure_Pa", "humidity_percent"]


def main():
    parser = argparse.ArgumentParser(description="Capture BME280 CSV data from Pico W serial output.")
    parser.add_argument("--port", required=True, help="Serial port, example: COM5")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--duration", type=int, default=60, help="Capture duration in seconds")
    parser.add_argument(
        "--output",
        default="data/raw/bme280_serial_log.csv",
        help="Output CSV file path",
    )

    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Opening serial port {args.port} at {args.baud} baud...")
    print(f"Saving data to {output_path}")
    print(f"Capture duration: {args.duration} seconds")

    rows_written = 0

    with serial.Serial(args.port, args.baud, timeout=2) as ser, open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(HEADER)

        time.sleep(2)
        ser.reset_input_buffer()

        start_time = time.time()

        while time.time() - start_time < args.duration:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            print(line)

            if line.startswith("time_s"):
                continue

            parts = line.split(",")

            if len(parts) == 4:
                writer.writerow(parts)
                rows_written += 1

    print(f"Done. Rows written: {rows_written}")
    print(f"Saved file: {output_path}")


if __name__ == "__main__":
    main()