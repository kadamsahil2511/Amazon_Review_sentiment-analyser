import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transforms import clean_text, is_usable_review, sentiment_from_polarity


class TransformTests(unittest.TestCase):
    def test_maps_polarity_labels(self):
        self.assertEqual(sentiment_from_polarity(1), "negative")
        self.assertEqual(sentiment_from_polarity(2), "positive")
        self.assertIsNone(sentiment_from_polarity(3))
        self.assertIsNone(sentiment_from_polarity(None))

    def test_cleans_escaped_newlines(self):
        self.assertEqual(clean_text("Good\\nproduct  "), "Good product")
        self.assertEqual(clean_text(None), "")

    def test_drops_empty_and_unlabeled_rows(self):
        self.assertTrue(is_usable_review("ok", "Lasted all week long", "positive"))
        self.assertFalse(is_usable_review("ok", "short", "positive"))
        self.assertFalse(is_usable_review("ok", "Lasted all week long", None))
        self.assertFalse(is_usable_review("ok", "", "negative"))


if __name__ == "__main__":
    unittest.main()
