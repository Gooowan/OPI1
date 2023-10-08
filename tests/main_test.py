import unittest
from unittest.mock import patch, Mock
from main import feature1, feature2, feature3


class TestMainFeatures(unittest.TestCase):

    @patch('main.collect_api_data')
    def test_feature1(self, mock_collect):

        mock_collect.return_value = [
            {"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"},
            {"userId": "2", "lastSeenDate": "2023-10-07T10:10:10"}
        ]
        online_count = feature1()
        self.assertEqual(online_count, 1)

    def test_feature2(self):

        global user_last_seen_data
        user_last_seen_data = {
            "1": ["2023-10-08T10:10:10", "2023-10-07T10:10:10"],
            "2": ["2023-10-06T10:10:10"]
        }
        result = feature2("2023-10-08T10:10:10", "1")
        self.assertEqual(result, {"wasUserOnline": True, "nearestOnlineTime": None})


if __name__ == '__main__':
    unittest.main()
