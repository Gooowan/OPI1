import os
import unittest
from unittest.mock import patch, Mock

from datetime import datetime

from api_utils import collect_api_data
from createdata import save_data_to_csv
from reports import adjusted_averageUserTime
from tests.test_integration import mock_collect_api_data
import api_utils


class TestApiUtilsE2E(unittest.TestCase):

    # E2E test for collecting data and making predictions
    @patch("api_utils.fetch_users_last_seen")
    @patch("api_utils.sleep", side_effect=lambda x: None)  # Mock sleep to prevent actual delay during tests
    def test_collect_and_predict_e2e(self, mock_sleep, mock_fetch_users_last_seen):
        # Mock the API responses for three data fetches
        mock_response_1 = Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {"data": [{"id": 1, "lastSeenDate": "2023-10-16T12:00:00"}]}

        mock_response_2 = Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {"data": [{"id": 2, "lastSeenDate": "2023-10-16T13:00:00"}]}

        mock_response_3 = Mock()
        mock_response_3.status_code = 200
        mock_response_3.json.return_value = {"data": [{"id": 3, "lastSeenDate": "2023-10-23T12:00:00"}]}

        mock_fetch_users_last_seen.side_effect = [mock_response_1, mock_response_2, mock_response_3]

        # Collect data for 3 iterations
        collected_data = api_utils.collect_api_data(max_iterations=3)

        # Make predictions for a specific user and date
        user_id = 1
        specified_date = datetime(2023, 10, 23, 12, 0, 0)
        online_chance = api_utils.predict_online_chance(user_id, specified_date, collected_data)
        average_online = api_utils.online_prediction(specified_date, collected_data)

        # Validate predictions
        self.assertEqual(online_chance, 0.0)  # Based on provided mock data
        self.assertEqual(average_online, 2 / 3)  # Based on provided mock data


class TestE2EReportGenerationWithFilename(unittest.TestCase):

    def setUp(self):
        # Define a sample filename for testing
        self.test_filename = "test_dataset_e2e.csv"

        # Ensure the test file doesn't exist before the test
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    @patch('api_utils.collect_api_data', mock_collect_api_data)
    def test_e2e_report_generation(self):
        # Collect a small sample of data using the mock function
        data = collect_api_data(delay_seconds=1, max_iterations=3)

        # Save the collected data to a CSV file
        save_data_to_csv(data, self.test_filename)

        # Generate a report using the saved data
        focus_user_id = 'user1'
        report = adjusted_averageUserTime(focus_user_id, filename=self.test_filename)

        # Check if the report contains data for the focus user
        self.assertIsNotNone(report)
        self.assertIn(focus_user_id, report)

        # Clean up the test file after the test
        os.remove(self.test_filename)
