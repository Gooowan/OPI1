
import unittest
from main import fetch_users_online_for_date, fetch_user_online_data

class TestFeatures(unittest.TestCase):
    
    def test_fetch_users_online_for_date(self):
        # Test with mock data (hardcoded value of 34 for any date)
        self.assertEqual(fetch_users_online_for_date("2023-27-09-20:00"), 34)

    def test_fetch_user_online_data(self):
        # Test with mock user ID and date
        user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
        date = "2023-27-09-20:00"
        expected_data = {
            "wasUserOnline": False,
            "nearestOnlineTime": "2023-28-09-15:00"
        }
        self.assertEqual(fetch_user_online_data(date, user_id), expected_data)
        
        # Test with a non-existing user ID
        non_existing_user_id = "NON-EXISTING-ID"
        expected_data = {
            "wasUserOnline": None,
            "nearestOnlineTime": None
        }
        self.assertEqual(fetch_user_online_data(date, non_existing_user_id), expected_data)

if __name__ == "__main__":
    unittest.main()
