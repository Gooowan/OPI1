import unittest
from unittest.mock import patch
from datetime import datetime
from time_utils import humanize_time_difference
from translations import translations

class TestHumanizeTimeDifference(unittest.TestCase):
    @patch('time_utils.datetime')
    def test_unknown_last_seen_date(self, mock_datetime):
        mock_datetime.utcnow.return_value = datetime(2023, 9, 30, 12, 0)
        self.assertEqual(humanize_time_difference(None), translations['en']['unknown'])
        self.assertEqual(humanize_time_difference(None, 'ua'), translations['ua']['unknown'])

    # ... Other tests continue in a similar fashion, mocking datetime.utcnow as needed
