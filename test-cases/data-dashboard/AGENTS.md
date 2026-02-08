# Agent Instructions — Water Quality Dashboard

Hey — I started building this but got pulled onto the permit review. Can you pick it up?

## What's here

`generate_report.py` reads the sensor CSV and computes daily averages. It works but only covers the basics (pH, turbidity, chlorine). I left TODOs where the trend analysis should go.

## What needs doing

1. Finish the `generate_trends()` function — it should compute 7-day rolling averages and flag any days where readings exceeded EPA limits
2. Add a summary section at the top of the report with overall status (compliant / needs attention / non-compliant)
3. Write the output to `output/report.md` as a readable markdown file

The EPA limits are already defined in the script. The data in `data/sensor_readings.csv` covers Jan–Mar from the new filtration system.

Don't overthink it — this is just for the internal weekly review meeting.
