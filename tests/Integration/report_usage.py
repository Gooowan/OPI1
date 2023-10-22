
import unittest
from reports import averageUserTime, compute_user_metrics, generate_report, get_report

class TestReportUsage(unittest.TestCase):

    def test_integration(self):
        # Generate a report
        report = generate_report('integration_report', ['dailyAverage', 'total'], [1], None, None)
        self.assertIn(1, report)

        # Retrieve the generated report
        retrieved_report = get_report('integration_report')
        self.assertEqual(report, retrieved_report)

        # Compute metrics for a user
        metrics = compute_user_metrics(1, ['dailyAverage', 'total'], None, None)
        self.assertIn('dailyAverage', metrics)
        self.assertIn('total', metrics)

        # Get average user time
        avg_daily, avg_weekly, daily_seconds, total_seconds = averageUserTime(1)
        self.assertIsInstance(avg_daily, float)
        self.assertIsInstance(avg_weekly, int)
        self.assertIsInstance(daily_seconds, list)
        self.assertIsInstance(total_seconds, int)

if __name__ == '__main__':
    unittest.main()
