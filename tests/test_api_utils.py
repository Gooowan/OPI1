import unittest
from unittest.mock import patch, Mock
from api_utils import fetch_users_last_seen


class TestFetchUsersLastSeen(unittest.TestCase):
    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen_404(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        response = fetch_users_last_seen(offset=0)
        self.assertEqual(response.status_code, 404)

    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen_500(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        response = fetch_users_last_seen(offset=0)
        self.assertEqual(response.status_code, 500)

    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen_malformed_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError  # Simulate a JSON decode error
        mock_get.return_value = mock_response
        with self.assertRaises(ValueError):  # Expecting a ValueError to be raised
            fetch_users_last_seen(offset=0)

    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen_unexpected_json_structure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'unexpectedKey': 'unexpectedValue'}  # Mocked unexpected data
        mock_get.return_value = mock_response
        response = fetch_users_last_seen(offset=0)
        self.assertEqual(response.json(), {'unexpectedKey': 'unexpectedValue'})
