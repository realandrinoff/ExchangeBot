from decimal import Decimal
import unittest

from amount import convert_amount


class TestConvertAmount(unittest.TestCase):
    def test_convert_amount(self):
        for amount, expected in [
            ("0000", Decimal(0)),
            ("100", Decimal(100)),
            ("100.0", Decimal(100)),
            ("100.003", Decimal("100.003")),
        ]:
            with self.subTest(amount=amount, expected=expected):
                self.assertEqual(convert_amount(amount), expected)

    def test_convert_amount_invalid(self):
        for amount in ["", "100.00.0", "100.00.00", "inf", "NaN", "-20", "abc"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    convert_amount(amount)

if __name__ == '__main__':
    unittest.main()
