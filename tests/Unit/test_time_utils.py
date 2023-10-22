import unittest
from unittest.mock import patch
from datetime import datetime
from time_utils import humanize_time_difference
from translations import translations


class TestHumanizeTimeDifference(unittest.TestCase):
    @patch('time_utils.datetime.datetime.utcnow')
    def test_just_now(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-30T11:59:31"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['just_now'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['just_now'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_less_than_a_minute_ago(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-30T11:59:10"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['less_minute'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['less_minute'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_couple_of_minutes_ago(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-30T11:10"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['couple_minutes'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['couple_minutes'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_hour_ago(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-30T10:45"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['hour_ago'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['hour_ago'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_today(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-30T09:30"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['today'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['today'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_yesterday(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-29T08:00"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['yesterday'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['yesterday'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_this_week(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2023-09-25T12:00"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['this_week'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['this_week'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_long_time_ago(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        last_seen = "2022-09-29T08:00"
        self.assertEqual(humanize_time_difference(last_seen), translations['en']['long_time_ago'])
        self.assertEqual(humanize_time_difference(last_seen, 'ua'), translations['ua']['long_time_ago'])

    @patch('time_utils.datetime.datetime.utcnow')
    def test_online(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        self.assertEqual(humanize_time_difference(None), translations['en']['online'])
        self.assertEqual(humanize_time_difference(None, 'ua'), translations['ua']['online'])
