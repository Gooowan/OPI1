import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from api_utils import collect_api_data
from createdata import save_data_to_csv

# Sample mock data to simulate the API response
mock_api_data = [
    {'userId': 'user1', 'lastSeenDate': datetime.utcnow().isoformat()},
    {'userId': 'user2', 'lastSeenDate': (datetime.utcnow() - timedelta(minutes=30)).isoformat()},
    {'userId': 'user3', 'lastSeenDate': (datetime.utcnow() - timedelta(hours=5)).isoformat()}
]


def mock_collect_api_data(delay_seconds=1, max_iterations=3):
    """Simulated function to mock the actual data collection"""
    return mock_api_data * max_iterations


class TestDataCollectionAndStorageWithFullMock(unittest.TestCase):

    def setUp(self):
        # Define a sample filename for testing
        self.test_filename = "test_dataset_mock.csv"

        # Ensure the test file doesn't exist before the test
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    @patch('api_utils.collect_api_data', mock_collect_api_data)
    def test_data_collection_and_storage(self):
        # Collect a small sample of data using the mock function
        data = collect_api_data(delay_seconds=1, max_iterations=3)

        # Save the collected data to a CSV file
        save_data_to_csv(data, self.test_filename)

        # Check if the file has been created
        self.assertTrue(os.path.exists(self.test_filename))

        # Check if the file contains data
        with open(self.test_filename, "r") as file:
            content = file.read()
            self.assertTrue(len(content) > 0)

import unittest
from unittest.mock import patch, Mock
from datetime import datetime
import api_utils


class TestApiUtilsIntegration(unittest.TestCase):

    # Test successful data collection using collect_api_data
    @patch("api_utils.fetch_users_last_seen")
    @patch("api_utils.sleep", side_effect=lambda x: None)  # Mock sleep to prevent actual delay during tests
    def test_collect_api_data_success(self, mock_sleep, mock_fetch_users_last_seen):
        # Mock the API responses for three successful data fetches
        mock_response_1 = Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {"data": [{"id": 1, "lastSeen": "2023-10-23T12:00:00"}]}

        mock_response_2 = Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {"data": [{"id": 2, "lastSeen": "2023-10-23T13:00:00"}]}

        mock_response_3 = Mock()
        mock_response_3.status_code = 200
        mock_response_3.json.return_value = {"data": [{"id": 3, "lastSeen": "2023-10-23T14:00:00"}]}

        mock_fetch_users_last_seen.side_effect = [mock_response_1, mock_response_2, mock_response_3]

        # Collect data for 3 iterations
        data = api_utils.collect_api_data(max_iterations=3)
        self.assertEqual(len(data), 3)  # Three data entries should be collected
    # Test failed data collection using collect_api_data due to API errors
    @patch("api_utils.fetch_users_last_seen")
    @patch("api_utils.sleep", side_effect=lambda x: None)  # Mock sleep to prevent actual delay during tests
    def test_collect_api_data_fail(self, mock_sleep, mock_fetch_users_last_seen):
        # Mock the API responses for three failed data fetches
        mock_response_1 = Mock()
        mock_response_1.status_code = 400
        mock_response_1.json.return_value = {"error": "Bad request"}

        mock_response_2 = Mock()
        mock_response_2.status_code = 500
        mock_response_2.json.return_value = {"error": "Internal server error"}

        mock_response_3 = Mock()
        mock_response_3.status_code = 404
        mock_response_3.json.return_value = {"error": "Not found"}

        mock_fetch_users_last_seen.side_effect = [mock_response_1, mock_response_2, mock_response_3]

        # Collect data for 3 iterations
        data = api_utils.collect_api_data(max_iterations=3)
        self.assertEqual(len(data), 0)  # No data entries should be collected due to errors

    # Test predict_online_chance function integration with historical data
    def test_predict_online_chance_integration(self):
        user_id = 1
        specified_date = datetime(2023, 10, 23, 12, 0, 0)

        # Historical data for two users
        user_last_seen_data = {
            1: [datetime(2023, 10, 16, 12, 0, 0), datetime(2023, 10, 9, 12, 0, 0)],
            2: [datetime(2023, 10, 16, 13, 0, 0)]
        }

        # User 1 was online at the same time in the previous two weeks
        chance = api_utils.predict_online_chance(user_id, specified_date, user_last_seen_data)
        self.assertEqual(chance, 7.0)

        # User 2 has different historical data
        chance = api_utils.predict_online_chance(2, specified_date, user_last_seen_data)
        self.assertEqual(chance, 0.0)

    # Test online_prediction function integration with user data
    def test_online_prediction_integration(self):
        specified_date = datetime(2023, 10, 23, 12, 0, 0)

        # Historical data for three users
        users_data = [
            {"id": 1, "lastSeenDate": "2023-10-16T12:00:00"},
            {"id": 2, "lastSeenDate": "2023-10-16T13:00:00"},
            {"id": 3, "lastSeenDate": "2023-10-23T12:00:00"}
        ]

        # 2 out of 3 users were online at the same time in the past
        average_online = api_utils.online_prediction(specified_date, users_data)
        self.assertEqual(average_online, 2 / 3)
