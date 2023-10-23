import unittest
from unittest.mock import patch, Mock

from datetime import datetime, timedelta

import api_utils
from time_utils import humanize_time_difference


class TestTimeUtils(unittest.TestCase):

    def setUp(self):
        # Setting the current UTC time for consistent tests
        self.current_utc = datetime.utcnow()

    def test_online_now(self):
        self.assertEqual(humanize_time_difference(None), "is online now")

    def test_just_now(self):
        timestamp = (self.current_utc - timedelta(seconds=10)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online just now")

    def test_less_than_minute(self):
        timestamp = (self.current_utc - timedelta(seconds=40)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online less than a minute ago")

    def test_couple_of_minutes(self):
        timestamp = (self.current_utc - timedelta(minutes=2)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online a couple of minutes ago")

    def test_unknown_timestamp(self):
        self.assertEqual(humanize_time_difference(""), "Unknown")

    def test_invalid_timestamp_format(self):
        self.assertEqual(humanize_time_difference("invalid_timestamp"), "Unknown time format")

    def test_about_an_hour_ago(self):
        timestamp = (self.current_utc - timedelta(minutes=110)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online an hour ago")

    def test_online_today(self):
        timestamp = (self.current_utc - timedelta(hours=4)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online today")

    def test_online_yesterday(self):
        timestamp = (self.current_utc - timedelta(days=1, hours=3)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online yesterday")

    def test_online_this_week(self):
        timestamp = (self.current_utc - timedelta(days=5)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online this week")

    def test_online_long_time_ago(self):
        timestamp = (self.current_utc - timedelta(days=10)).isoformat()
        self.assertEqual(humanize_time_difference(timestamp), "was online a long time ago")


class TestApiUtils(unittest.TestCase):

    # Test fetch_users_last_seen function
    @patch("api_utils.requests.get")
    def test_fetch_users_last_seen(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1, "lastSeen": "2023-10-23T12:00:00"}]}
        mock_get.return_value = mock_response

        # Test the function
        response = api_utils.fetch_users_last_seen()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": [{"id": 1, "lastSeen": "2023-10-23T12:00:00"}]})

    @patch("api_utils.fetch_users_last_seen")
    @patch("api_utils.sleep", side_effect=lambda x: None)  # Mock sleep to prevent actual delay during tests
    def test_collect_api_data(self, mock_sleep, mock_fetch_users_last_seen):
        # Mock the API response for successful data fetch
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"data": [{"id": 1, "lastSeen": "2023-10-23T12:00:00"}]}

        # Mock the API response for failed data fetch
        mock_response_fail = Mock()
        mock_response_fail.status_code = 400
        mock_response_fail.json.return_value = {"error": "Bad request"}

        # Scenario 1: Successful data collection for 2 iterations
        mock_fetch_users_last_seen.side_effect = [mock_response_success, mock_response_success]
        data = api_utils.collect_api_data(max_iterations=2)
        self.assertEqual(len(data), 2)

        # Scenario 2: One successful and one failed data collection
        mock_fetch_users_last_seen.side_effect = [mock_response_success, mock_response_fail]
        data = api_utils.collect_api_data(max_iterations=2)
        self.assertEqual(len(data), 1)

    # Test predict_online_chance function
    def test_predict_online_chance(self):
        user_id = 1
        specified_date = datetime(2023, 10, 23, 12, 0, 0)
        user_last_seen_data = {
            1: [datetime(2023, 10, 16, 12, 0, 0), datetime(2023, 10, 9, 12, 0, 0)]
        }

        # User was online at the same time in the previous two weeks
        chance = api_utils.predict_online_chance(user_id, specified_date, user_last_seen_data)
        self.assertEqual(chance, 7.0)  # 2 occurrences in the past 2 weeks

        # User has no historical data
        chance = api_utils.predict_online_chance(2, specified_date, user_last_seen_data)
        self.assertEqual(chance, 0.0)

    # Test online_prediction function
    def test_online_prediction(self):
        specified_date = datetime(2023, 10, 23, 12, 0, 0)
        users_data = [
            {"id": 1, "lastSeenDate": "2023-10-16T12:00:00"},
            {"id": 2, "lastSeenDate": "2023-10-16T13:00:00"},
            {"id": 3, "lastSeenDate": "2023-10-23T12:00:00"}
        ]

        # 2 out of 3 users were online at the same time in the past
        average_online = api_utils.online_prediction(specified_date, users_data)
        self.assertEqual(average_online, 2 / 3)
