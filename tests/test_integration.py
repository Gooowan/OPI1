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
