import unittest


from fuzzy import Fuzzy


class TestFuzzy(unittest.TestCase):
    def test_integrity(self):
        fuzzy = Fuzzy()
        self.assertTrue(hasattr(fuzzy, "collections"))
        self.assertTrue(hasattr(fuzzy, "search"))
        self.assertTrue(hasattr(fuzzy, "calculate_score"))
