import unittest
import requests_mock
from main2 import get_users


class TestUserListAPI(unittest.TestCase):
    @requests_mock.Mocker()
    def test_fetch_users_error(self, mock):
        mock.get("https://sef.podkolzin.consulting/api/users/lastSeen?offset=0", status_code=500)

        response, status_code = get_users()

        self.assertEqual(status_code, 500)


if __name__ == '__main__':
    unittest.main()
