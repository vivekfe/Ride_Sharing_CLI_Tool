import unittest
from SalaryCalculator import SalaryCalculator


class TestCalculateSalary(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_driver_payment(self):
        x = SalaryCalculator()
        y = x.calculate_driver_payment(1, '2022-01-01', '2022-01-31')
        self.assertEqual(y, 4)


if __name__ == '__main__':
    unittest.main()
