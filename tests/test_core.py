"""Tests for farey_sequence_generator.core.

Run with:

    PYTHONPATH=src python -m unittest discover -s tests
"""

import unittest

from farey_sequence_generator import (
    FareyFraction,
    generate_farey_sequence,
    farey_length,
)


class TestFareyFraction(unittest.TestCase):
    def test_basic_construction(self):
        f = FareyFraction(1, 2)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_value(self):
        self.assertAlmostEqual(FareyFraction(1, 2).value(), 0.5)
        self.assertAlmostEqual(FareyFraction(0, 1).value(), 0.0)
        self.assertAlmostEqual(FareyFraction(3, 4).value(), 0.75)

    def test_zero_fraction_allowed(self):
        f = FareyFraction(0, 5)
        self.assertEqual(f.numerator, 0)
        self.assertEqual(f.value(), 0.0)

    def test_negative_denominator_rejected(self):
        with self.assertRaises(ValueError):
            FareyFraction(1, -2)

    def test_zero_denominator_rejected(self):
        with self.assertRaises(ValueError):
            FareyFraction(1, 0)

    def test_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            FareyFraction(2, 1)  # equal to 1, not in [0, 1)
        with self.assertRaises(ValueError):
            FareyFraction(3, 2)  # greater than 1
        with self.assertRaises(ValueError):
            FareyFraction(-1, 2)  # negative

    def test_frozen(self):
        f = FareyFraction(1, 2)
        with self.assertRaises(Exception):
            f.numerator = 3  # type: ignore[misc]


class TestGenerateFareySequence(unittest.TestCase):
    def test_order_1(self):
        seq = generate_farey_sequence(1)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 1)])

    def test_order_2(self):
        seq = generate_farey_sequence(2)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 2), (1, 1)])

    def test_order_3(self):
        seq = generate_farey_sequence(3)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 3), (1, 2), (2, 3), (1, 1)])

    def test_order_5(self):
        seq = generate_farey_sequence(5)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 5), (1, 4), (1, 3), (2, 5),
                          (1, 2), (3, 5), (2, 3), (3, 4), (4, 5), (1, 1)])

    def test_order_6(self):
        seq = generate_farey_sequence(6)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 6), (1, 5), (1, 4), (1, 3),
                          (2, 5), (1, 2), (3, 5), (2, 3), (3, 4),
                          (4, 5), (5, 6), (1, 1)])

    def test_invalid_order_zero(self):
        with self.assertRaises(ValueError):
            generate_farey_sequence(0)

    def test_invalid_order_negative(self):
        with self.assertRaises(ValueError):
            generate_farey_sequence(-3)

    def test_first_and_last_terms(self):
        for n in [1, 2, 5, 10, 20]:
            seq = generate_farey_sequence(n)
            self.assertEqual((seq[0].numerator, seq[0].denominator), (0, 1))
            self.assertEqual((seq[-1].numerator, seq[-1].denominator), (1, 1))

    def test_terms_are_sorted(self):
        for n in [1, 2, 5, 10, 25]:
            seq = generate_farey_sequence(n)
            values = [f.value() for f in seq]
            for i in range(1, len(values)):
                self.assertGreater(values[i], values[i - 1],
                                   f"not sorted at n={n}, index {i}")

    def test_all_fractions_reduced(self):
        from math import gcd
        for n in [1, 2, 5, 10, 25]:
            seq = generate_farey_sequence(n)
            for f in seq:
                self.assertEqual(
                    gcd(f.numerator, f.denominator), 1,
                    f"{f.numerator}/{f.denominator} not reduced at n={n}",
                )

    def test_mediant_property(self):
        # For consecutive a/b, c/d in a Farey sequence: b*c - a*d == 1.
        for n in [1, 2, 5, 10, 25]:
            seq = generate_farey_sequence(n)
            for i in range(len(seq) - 1):
                a, b = seq[i].numerator, seq[i].denominator
                c, d = seq[i + 1].numerator, seq[i + 1].denominator
                self.assertEqual(b * c - a * d, 1,
                                 f"mediant property fails at n={n}, index {i}")

    def test_denominators_within_bound(self):
        for n in [1, 2, 5, 10, 25]:
            seq = generate_farey_sequence(n)
            for f in seq:
                self.assertLessEqual(f.denominator, n,
                                     f"denominator {f.denominator} exceeds n={n}")

    def test_length_matches_direct_formula(self):
        for n in [1, 2, 3, 5, 10, 15]:
            seq = generate_farey_sequence(n)
            self.assertEqual(len(seq), farey_length(n),
                             f"length mismatch at n={n}")

    def test_order_4(self):
        seq = generate_farey_sequence(4)
        self.assertEqual([(f.numerator, f.denominator) for f in seq],
                         [(0, 1), (1, 4), (1, 3), (1, 2),
                          (2, 3), (3, 4), (1, 1)])


class TestFareyLength(unittest.TestCase):
    def test_known_values(self):
        # F_1 = 2 terms, F_2 = 3, F_3 = 5, F_4 = 7, F_5 = 11, F_6 = 13
        self.assertEqual(farey_length(1), 2)
        self.assertEqual(farey_length(2), 3)
        self.assertEqual(farey_length(3), 5)
        self.assertEqual(farey_length(4), 7)
        self.assertEqual(farey_length(5), 11)
        self.assertEqual(farey_length(6), 13)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            farey_length(0)
        with self.assertRaises(ValueError):
            farey_length(-1)


class TestPackageExports(unittest.TestCase):
    def test_all_exports_exist(self):
        import farey_sequence_generator as pkg
        for name in pkg.__all__:
            self.assertTrue(hasattr(pkg, name), f"missing export: {name}")


if __name__ == "__main__":
    unittest.main()
