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
