import unittest
from datetime import datetime
from unittest.mock import patch, Mock
from api_utils import fetch_users_last_seen, collect_api_data, predict_online_chance, online_prediction


class TestApiUtils(unittest.TestCase):

    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]}
        mock_get.return_value = mock_response

        response = fetch_users_last_seen()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]})

    @patch('api_utils.fetch_users_last_seen')
    def test_collect_api_data(self, mock_fetch):
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]}

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"data": []}

        mock_fetch.side_effect = [mock_response1, mock_response2]

        data = collect_api_data(delay_seconds=0, max_iterations=5)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"})


class TestPrediction(unittest.TestCase):

    def setUp(self):
        # Sample historical data for testing
        self.user_last_seen_data = {
            1: [datetime(2023, 1, 3, 15, 0), datetime(2023, 1, 10, 15, 0), datetime(2023, 1, 17, 15, 5)]
        }

    def test_predict_online_chance(self):
        # User was online on three Tuesdays around 3 PM
        chance = predict_online_chance(1, datetime(2023, 1, 24, 15, 0), self.user_last_seen_data)
        self.assertAlmostEqual(chance, 3 / 3, places=2)  # Expected 100% chance

        # Predicting for a time when user has never been online
        chance = predict_online_chance(1, datetime(2023, 1, 24, 20, 0), self.user_last_seen_data)
        self.assertAlmostEqual(chance, 0, places=2)  # Expected 0% chance

        # Predicting for a user with no historical data
        chance = predict_online_chance(2, datetime(2023, 1, 24, 15, 0), self.user_last_seen_data)
        self.assertAlmostEqual(chance, 0, places=2)  # Expected 0% chance


class TestOnlinePrediction(unittest.TestCase):

    def setUp(self):
        # Sample historical data for testing
        self.users_data = [
            {'userId': 1, 'lastSeenDate': '2023-01-03T15:00:00'},
            {'userId': 2, 'lastSeenDate': '2023-01-03T15:00:00'},
            {'userId': 3, 'lastSeenDate': '2023-01-10T15:05:00'},
            {'userId': 4, 'lastSeenDate': '2023-01-10T16:00:00'}
        ]

    def test_online_prediction(self):
        # On 2023-01-03 at 15:00, two users were online
        avg_online = online_prediction(datetime(2023, 1, 24, 15, 0), self.users_data)
        self.assertAlmostEqual(avg_online, 2 / 4, places=2)  # Expected 50% users online

        # On 2023-01-10 at 16:00, one user was online
        avg_online = online_prediction(datetime(2023, 1, 24, 16, 0), self.users_data)
        self.assertAlmostEqual(avg_online, 1 / 4, places=2)  # Expected 25% users online


if __name__ == '__main__':
    unittest.main()
