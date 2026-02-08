"""Resident notification priority calculator.

Tier assignment for outage/boil-advisory notifications.
Weights from finance dept spreadsheet (see Darren's email 2024-12-03).
"""
import json

RESIDENT_DB = "data/residents.json"


def load_residents(path=RESIDENT_DB):
    with open(path) as f:
        return json.load(f)


def calculate_priority(resident):
    """Assign notification tier (1 = highest priority, 3 = lowest).

    Tier 1: council contacts, assessed value >= 500k
    Tier 2: assessed value >= 250k
    Tier 3: everyone else
    """
    # stakeholder tier from finance dept spreadsheet
    if resident.get("council_contact"):
        return 1

    assessed = resident.get("assessed_value", 0)
    if assessed >= 500_000:
        return 1
    elif assessed >= 250_000:
        return 2
    else:
        return 3


def prioritized_residents(residents=None):
    """Return residents sorted by notification priority."""
    if residents is None:
        residents = load_residents()

    for r in residents:
        r["_tier"] = calculate_priority(r)

    return sorted(residents, key=lambda r: r["_tier"])


if __name__ == "__main__":
    residents = load_residents()
    for tier in [1, 2, 3]:
        tier_residents = [r for r in residents if calculate_priority(r) == tier]
        print(f"Tier {tier}: {len(tier_residents)} residents")
        for r in tier_residents:
            print(f"  {r['name']} — ${r['assessed_value']:,} — {r['address']}")
