import unittest

from invoice import totals


class InvoiceTest(unittest.TestCase):
    def test_totals(self):
        owed = totals("orders.csv")
        self.assertAlmostEqual(owed["Ada"], 20.00)  # 4 x 2.50 + 1 x 10.00
        self.assertAlmostEqual(owed["Ben"], 37.00)  # 2 x 7.25 + 10 x 2.50, less 10% on the 10


if __name__ == "__main__":
    unittest.main()
