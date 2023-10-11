import unittest
from unittest.mock import patch
from main import totalUserMinutes, averageUserTime


class TestUserTimeFunctions(unittest.TestCase):

    @patch('main.collect_api_data')
    def test_totalUserMinutes_single_entry(self, mock_collect_api_data):
        # Mock data: User was online once within the last minute
        mock_collect_api_data.return_value = [{'userId': 'sample_user', 'lastSeenDate': '2023-10-11T12:00:00'}]

        user_id = 'sample_user'
        result = totalUserMinutes(user_id)
        self.assertEqual(result, 1)

    @patch('main.collect_api_data')
    def test_totalUserMinutes_no_entry(self, mock_collect_api_data):
        # Mock data: User wasn't online within the last minute
        mock_collect_api_data.return_value = []

        user_id = 'sample_user'
        result = totalUserMinutes(user_id)
        self.assertEqual(result, 0)

    @patch('main.collect_api_data')
    def test_averageUserTime_daily_average(self, mock_collect_api_data):
        # Mock data: User was online for 5 seconds every day for a week
        mock_data = [{'userId': 'sample_user', 'lastSeenDate': f'2023-10-11T12:00:0{i}'} for i in range(5)]
        mock_collect_api_data.return_value = mock_data * 7

        user_id = 'sample_user'
        daily_avg, weekly_avg = averageUserTime(user_id)
        self.assertEqual(daily_avg, 5)
        self.assertEqual(weekly_avg, 35)

    @patch('main.collect_api_data')
    def test_averageUserTime_no_activity(self, mock_collect_api_data):
        # Mock data: User wasn't online at all for a week
        mock_collect_api_data.return_value = []

        user_id = 'sample_user'
        daily_avg, weekly_avg = averageUserTime(user_id)
        self.assertEqual(daily_avg, 0)
        self.assertEqual(weekly_avg, 0)


if __name__ == "__main__":
    unittest.main()


class IntegrationTestUserTimeFunctions(unittest.TestCase):

    def setUp(self):
        # This method will run before each test. You can use it to set up any shared resources.
        self.user_id = 'sample_user'

    def test_integration_totalUserMinutes(self):
        # This test checks if the totalUserMinutes function can correctly fetch and process data from the data source.
        minutes = totalUserMinutes(self.user_id)

        # For demonstration, we're just checking the return type. In a real-world scenario,
        # you might want to set up a known data state and then verify the results.
        self.assertTrue(isinstance(minutes, int))

    def test_integration_averageUserTime(self):
        # This test checks if the averageUserTime function can correctly fetch and process data from the data source.
        daily_avg, weekly_avg = averageUserTime(self.user_id)

        # Again, we're checking return types for demonstration. Depending on your setup,
        # you might want to compare against expected averages.
        self.assertTrue(isinstance(daily_avg, (int, float)))
        self.assertTrue(isinstance(weekly_avg, (int, float)))

    def tearDown(self):
        # This method will run after each test. You can use it to tear down or clean up any shared resources.
        pass


if __name__ == "__main__":
    unittest.main()
