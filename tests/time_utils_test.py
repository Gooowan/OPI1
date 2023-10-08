import unittest
from datetime import datetime, timedelta
from time_utils import humanize_time_difference


class TestTimeUtils(unittest.TestCase):

    def test_humanize_time_difference_en(self):

        now = datetime.utcnow()

        date_str = (now - timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online just now")

        date_str = (now - timedelta(seconds=40)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online less than a minute ago")

        date_str = (now - timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online a couple of minutes ago")

        date_str = (now - timedelta(minutes=70)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online an hour ago")

        date_str = (now - timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online today")

        date_str = (now - timedelta(days=1, hours=5)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online yesterday")

        date_str = (now - timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online this week")

        date_str = (now - timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(humanize_time_difference(date_str, 'en'), "was online a long time ago")


if __name__ == '__main__':
    unittest.main()
