import unittest
from unittest.mock import patch, Mock
from api_utils import fetch_users_last_seen

class TestFetchUsersLastSeen(unittest.TestCase):
    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [...] }  # Mocked data
        mock_get.return_value = mock_response
        response = fetch_users_last_seen(offset=0)
        self.assertEqual(response.status_code, 200)
        # ... Additional assertions for the mocked response
