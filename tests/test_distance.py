import unittest

from line_align.pylib.levenshtein import levenshtein


class TestDistance(unittest.TestCase):
    def test_distance_01(self):
        self.assertEqual(levenshtein("aa", "bb"), 2)

    def test_distance_02(self):
        self.assertEqual(levenshtein("ab", "bb"), 1)

    def test_distance_03(self):
        self.assertEqual(levenshtein("ab", "ab"), 0)

    def test_distance_04(self):
        self.assertEqual(levenshtein("aa", "aba"), 1)

    def test_distance_05(self):
        self.assertEqual(levenshtein("aa", "baa"), 1)

    def test_distance_06(self):
        self.assertEqual(levenshtein("aa", "aab"), 1)

    def test_distance_07(self):
        self.assertEqual(levenshtein("baa", "aa"), 1)

    def test_distance_08(self):
        self.assertEqual(levenshtein("aab", "aa"), 1)

    def test_distance_09(self):
        self.assertEqual(levenshtein("baab", "aa"), 2)

    def test_distance_10(self):
        self.assertEqual(levenshtein("aa", "baab"), 2)

    def test_distance_11(self):
        self.assertEqual(levenshtein("", "aa"), 2)

    def test_distance_12(self):
        self.assertEqual(levenshtein("aa", ""), 2)

    def test_distance_13(self):
        self.assertEqual(levenshtein("", ""), 0)

    def test_distance_14(self):
        self.assertEqual(1, levenshtein("aa", "五aa"))

    def test_distance_15(self):
        self.assertEqual(1, levenshtein("五aa", "aa"))

    def test_distance_16(self):
        self.assertEqual(1, levenshtein("aa", "aa五"))

    def test_distance_17(self):
        self.assertEqual(1, levenshtein("aa五", "aa"))

    def test_distance_18(self):
        self.assertEqual(1, levenshtein("a五a", "aa"))

    def test_distance_19(self):
        self.assertEqual(1, levenshtein("aa", "a五a"))

    def test_distance_20(self):
        self.assertEqual(1, levenshtein("五五", "五六"))

    def test_distance_21(self):
        self.assertEqual(0, levenshtein("五五", "五五"))

    def test_distance_22(self):
        self.assertEqual(levenshtein("123aa4", "aa"), 4)

    def test_distance_23(self):
        self.assertEqual(levenshtein("aa", "1aa234"), 4)

    def test_distance_24(self):
        self.assertEqual(levenshtein("aa", "a123a"), 3)

    def test_distance_25(self):
        self.assertEqual(levenshtein("aa", "12345aa"), 5)

    def test_distance_26(self):
        self.assertEqual(
            levenshtein("Commelinaceae Commelina virginica", "Commelina virginica"),
            14,
        )

    def test_distance_27(self):
        self.assertEqual(
            levenshtein(
                "North Carolina NORTH CAROLINA Guilford County",
                "North Carolina OT CAROLINA Guilford County",
            ),
            3,
        )
