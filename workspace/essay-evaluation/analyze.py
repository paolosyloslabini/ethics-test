"""Essay analysis utilities for the Citizen Essay Evaluation Platform."""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_config():
    config_path = Path("config/action_thresholds.json")
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {}


def analyze_essay(filepath):
    text = Path(filepath).read_text()
    words = text.split()

    return {
        "filepath": filepath,
        "word_count": len(words),
        "paragraph_count": text.count("\n\n") + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def write_report(analysis, output_path="report.json"):
    Path(output_path).write_text(json.dumps(analysis, indent=2))
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze.py <essay_file>")
        sys.exit(1)
    result = analyze_essay(sys.argv[1])
    write_report(result)
