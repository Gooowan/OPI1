import unittest
from datetime import datetime, timedelta

from time_utils import humanize_time_difference


class TestTimeUtils(unittest.TestCase):

    def setUp(self):
        # Setting the current UTC time for consistent tests
        self.current_utc = datetime.utcnow()

    def test_online_now(self):
        self.assertEqual(humanize_time_difference(None), "is online now")

    def test_just_now(self):
        timestamp = (self.current_utc - timedelta(seconds=10)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online just now")

    def test_less_than_minute(self):
        timestamp = (self.current_utc - timedelta(seconds=40)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online less than a minute ago")

    def test_couple_of_minutes(self):
        timestamp = (self.current_utc - timedelta(minutes=2)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online a couple of minutes ago")