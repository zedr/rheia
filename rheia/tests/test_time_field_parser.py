import unittest

from rheia.parsers.time import parse_time, time_sequence_rxp


class TimeFieldParserTests(unittest.TestCase):
    """Tests for the time field parser.
    """

    def test_pattern_matched_correct_syntax(self):
        self.assertTrue(
            time_sequence_rxp.match("1h 20m 5s")
        )
        self.assertTrue(
            time_sequence_rxp.match("20m 5s ")
        )
        self.assertTrue(
            time_sequence_rxp.match("5s ")
        )

    def test_can_parse_hours_as_seconds(self):
        seconds = parse_time("6h")
        self.assertEqual(seconds, 6 * 60 * 60)

    def test_can_parse_minutes_as_seconds(self):
        seconds = parse_time("20m")
        self.assertEqual(seconds, 20 * 60)

    def test_can_parse_seconds_as_seconds(self):
        seconds = parse_time("60s")
        self.assertEqual(seconds, 60)

    def test_can_parse_composite_time_as_seconds(self):
        seconds = parse_time("1h 20m 120s")
        self.assertEqual(seconds, 4920)
