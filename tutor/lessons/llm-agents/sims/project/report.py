import csv


def revenue_by_region(path):
    """Total revenue (units times unit price) for each region in a sales CSV."""
    totals = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            region = row["region"]
            totals[region] = totals.get(region, 0) + int(row["units"]) + float(row["unit_price"])
    return totals
