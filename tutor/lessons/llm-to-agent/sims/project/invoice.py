"""Print what each customer owes for the orders in a CSV file."""
import csv
import sys

from prices import price_of

BULK = 10
DISCOUNT = 0.10


def totals(path):
    owed = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            quantity = int(row["quantity"])
            cost = quantity * price_of(row["product"])
            if quantity > BULK:
                cost = cost * (1 - DISCOUNT)
            owed[row["customer"]] = owed.get(row["customer"], 0) + cost
    return owed


if __name__ == "__main__":
    for customer, amount in totals(sys.argv[1]).items():
        print(f"{customer}: {amount:.2f}")
