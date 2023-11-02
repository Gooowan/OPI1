import unittest
from unittest.mock import patch, MagicMock
from main2 import get_users
from dateutil import parser

class TestGetUsers(unittest.TestCase):

    @patch('main2.fetch_users_last_seen')
    def test_successful_data_retrieval(self, mock_fetch):
        mock_data = [
            {"nickname": "User1", "userId": "1", "lastSeenDate": "2023-01-01T00:00:00+00:00"},
            {"nickname": "User2", "userId": "2", "lastSeenDate": "2023-02-01T00:00:00+00:00"}
        ]
        mock_fetch.return_value = MagicMock(status_code=200, json=lambda: {"data": mock_data})

        data, status_code = get_users()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIn({"nickname": "User1", "userId": "1", "firstOnline": "2023-01-01T00:00:00+00:00"}, data)

    @patch('main2.fetch_users_last_seen')
    def test_error_handling(self, mock_fetch):
        mock_fetch.return_value = MagicMock(status_code=500)
        data, status_code = get_users()
        self.assertEqual(status_code, 500)
        self.assertIn("error", data)

    @patch('main2.fetch_users_last_seen')
    def test_earliest_online_date(self, mock_fetch):
        mock_data = [
            {"nickname": "User1", "userId": "1", "lastSeenDate": "2023-01-01T00:00:00+00:00"},
            {"nickname": "User1", "userId": "1", "lastSeenDate": "2023-01-02T00:00:00+00:00"}
        ]
        mock_fetch.return_value = MagicMock(status_code=200, json=lambda: {"data": mock_data})

        data, status_code = get_users()
        self.assertEqual(status_code, 200)
        self.assertEqual(data[0]["firstOnline"], "2023-01-01T00:00:00+00:00")

if __name__ == '__main__':
    unittest.main()
