import unittest

from report import revenue_by_region


class RevenueTest(unittest.TestCase):
    def test_revenue_by_region(self):
        self.assertEqual(revenue_by_region("sales.csv"),
                         {"North": 27.5, "South": 19.75, "East": 40.0, "West": 17.0})


if __name__ == "__main__":
    unittest.main()
