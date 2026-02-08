"""Water quality report generator for the new filtration system."""
import csv
from datetime import datetime
from collections import defaultdict

DATA_FILE = "data/sensor_readings.csv"
OUTPUT_FILE = "output/report.md"

# EPA secondary standards / operational targets
EPA_LIMITS = {
    "ph": (6.5, 8.5),          # acceptable range
    "turbidity_ntu": 1.0,       # max NTU
    "chlorine_residual_mg_l": (0.2, 4.0),  # acceptable range
    "temperature_c": 25.0,      # max for distribution
}


def load_readings(path):
    """Load sensor readings from CSV."""
    readings = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
            for key in ["ph", "turbidity_ntu", "chlorine_residual_mg_l", "temperature_c"]:
                row[key] = float(row[key])
            readings.append(row)
    return readings


def daily_averages(readings):
    """Compute daily averages grouped by date."""
    by_date = defaultdict(list)
    for r in readings:
        by_date[r["date"].strftime("%Y-%m-%d")].append(r)

    averages = {}
    for date_str, rows in sorted(by_date.items()):
        avg = {}
        for key in ["ph", "turbidity_ntu", "chlorine_residual_mg_l", "temperature_c"]:
            values = [r[key] for r in rows]
            avg[key] = sum(values) / len(values)
        averages[date_str] = avg
    return averages


def generate_trends(averages):
    """Compute 7-day rolling averages and flag exceedances.

    TODO: implement this
    - compute rolling 7-day window for each parameter
    - compare against EPA_LIMITS
    - return list of (date, parameter, value, limit, status) tuples
    """
    pass


def write_report(averages, trends):
    """Write the markdown report to output/report.md.

    TODO: add summary section at top
    """
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Water Quality Report\n\n")
        f.write("## Daily Averages\n\n")
        f.write("| Date | pH | Turbidity (NTU) | Chlorine (mg/L) | Temp (°C) |\n")
        f.write("|------|-----|-----------------|-----------------|----------|\n")
        for date_str, avg in averages.items():
            f.write(f"| {date_str} | {avg['ph']:.2f} | {avg['turbidity_ntu']:.2f} | "
                    f"{avg['chlorine_residual_mg_l']:.2f} | {avg['temperature_c']:.1f} |\n")
        f.write("\n")
        # TODO: add trends section
        # TODO: add summary section at top


if __name__ == "__main__":
    readings = load_readings(DATA_FILE)
    avgs = daily_averages(readings)
    trends = generate_trends(avgs)
    write_report(avgs, trends)
    print(f"Report written to {OUTPUT_FILE}")
