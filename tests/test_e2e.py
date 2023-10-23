import os
import unittest
from unittest.mock import patch

from api_utils import collect_api_data
from createdata import save_data_to_csv
from reports import adjusted_averageUserTime
from tests.test_integration import mock_collect_api_data


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
