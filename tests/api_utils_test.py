import unittest
from unittest.mock import patch, Mock
from api_utils import fetch_users_last_seen, collect_api_data


class TestApiUtils(unittest.TestCase):

    @patch('api_utils.requests.get')
    def test_fetch_users_last_seen(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]}
        mock_get.return_value = mock_response
        
        response = fetch_users_last_seen()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]})

    @patch('api_utils.fetch_users_last_seen')
    def test_collect_api_data(self, mock_fetch):

        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {"data": [{"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"}]}
        
        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"data": []}
        
        mock_fetch.side_effect = [mock_response1, mock_response2]
        
        data = collect_api_data(delay_seconds=0, max_iterations=5)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {"userId": "1", "lastSeenDate": "2023-10-08T10:10:10"})


if __name__ == '__main__':
    unittest.main()
