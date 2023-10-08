
import unittest
from time_utils import humanize_time_difference
from datetime import datetime, timedelta

class TestTimeUtils(unittest.TestCase):

    def test_humanize_time_difference_online(self):
        self.assertEqual(humanize_time_difference(None, 'en'), "is online now")

    def test_humanize_time_difference_unknown(self):
        self.assertEqual(humanize_time_difference("", 'en'), "Unknown")
        self.assertEqual(humanize_time_difference("invalid format", 'en'), "Unknown time format")

    def test_humanize_time_difference_just_now(self):
        now = datetime.utcnow().isoformat()
        self.assertEqual(humanize_time_difference(now, 'en'), "was online just now")

    def test_humanize_time_difference_less_than_minute(self):
        less_than_minute = (datetime.utcnow() - timedelta(seconds=45)).isoformat()
        self.assertEqual(humanize_time_difference(less_than_minute, 'en'), "was online less than a minute ago")

    def test_humanize_time_difference_today(self):
        today = (datetime.utcnow() - timedelta(hours=2)).isoformat()
        self.assertEqual(humanize_time_difference(today, 'en'), "was online today")

    def test_humanize_time_difference_yesterday(self):
        yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()
        self.assertEqual(humanize_time_difference(yesterday, 'en'), "was online yesterday")

    def test_humanize_time_difference_this_week(self):
        this_week = (datetime.utcnow() - timedelta(days=5)).isoformat()
        self.assertEqual(humanize_time_difference(this_week, 'en'), "was online this week")

    def test_humanize_time_difference_long_time_ago(self):
        long_time_ago = (datetime.utcnow() - timedelta(days=10)).isoformat()
        self.assertEqual(humanize_time_difference(long_time_ago, 'en'), "was online a long time ago")

if __name__ == "__main__":
    unittest.main()



import unittest
from unittest.mock import patch, Mock
import main

class TestMainIntegration(unittest.TestCase):

    @patch('builtins.input')
    @patch('main.fetch_users_last_seen')
    def test_feature1(self, mock_fetch, mock_input):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [
            {'userId': '123', 'lastSeenDate': '2023-10-08T12:34:56'},
            {'userId': '456', 'lastSeenDate': None}
        ]}
        mock_fetch.return_value = mock_response

        mock_input.side_effect = ["en", "1", "exit"]

        with self.assertLogs() as log:
            main.main()

        self.assertIn("There are 1 users online right now.", log.output)


if __name__ == "__main__":
    unittest.main()
