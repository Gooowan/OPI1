
import unittest
from unittest.mock import patch
from reports import averageUserTime, compute_user_metrics, generate_report, get_report

class TestReports(unittest.TestCase):

    # Mock data for collect_api_data function
    mock_data = [
        {'userId': 1, 'lastSeenDate': '2023-10-15'},
        {'userId': 1, 'lastSeenDate': '2023-10-16'},
        {'userId': 2, 'lastSeenDate': '2023-10-14'},
        {'userId': 3, 'lastSeenDate': '2023-10-17'}
    ]

    @patch('reports.collect_api_data', return_value=mock_data)
    def test_averageUserTime(self, _):
        avg_daily, avg_weekly, daily_seconds, total_seconds = averageUserTime(1)
        self.assertEqual(avg_daily, 2/7)
        self.assertEqual(avg_weekly, 2)
        self.assertEqual(daily_seconds, [0, 0, 0, 0, 1, 1, 0])
        self.assertEqual(total_seconds, 2)

    @patch('reports.averageUserTime', return_value=(2/7, 2, [0, 0, 0, 0, 1, 1, 0], 2))
    def test_compute_user_metrics(self, _):
        metrics = compute_user_metrics(1, ['dailyAverage', 'total'], None, None)
        self.assertEqual(metrics['dailyAverage'], 2/7)
        self.assertEqual(metrics['total'], 2)

    @patch('reports.compute_user_metrics', return_value={'dailyAverage': 2/7, 'total': 2})
    def test_generate_report(self, _):
        report = generate_report('test_report', ['dailyAverage', 'total'], [1], None, None)
        self.assertIn(1, report)
        self.assertEqual(report[1]['dailyAverage'], 2/7)
        self.assertEqual(report[1]['total'], 2)

    @patch('reports.all_reports', {'test_report': {1: {'dailyAverage': 2/7, 'total': 2}}})
    def test_get_report(self):
        report = get_report('test_report')
        self.assertIn(1, report)
        self.assertEqual(report[1]['dailyAverage'], 2/7)
        self.assertEqual(report[1]['total'], 2)

if __name__ == '__main__':
    unittest.main()
