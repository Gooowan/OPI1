from datetime import datetime
import pandas as pd
from api_utils import collect_api_data
import csv

# Global variable to store all reports
all_reports = {}

# Constants
DAYS_IN_WEEK = 7

dataset_df = pd.read_csv("dataset.csv")

def averageUserTime(focus_user_id):
    users_data = collect_api_data(delay_seconds=1, max_iterations=DAYS_IN_WEEK * 24 * 60 * 60)
    daily_seconds = [0 for _ in range(DAYS_IN_WEEK)]
    total_seconds = 0
    current_time = datetime.utcnow()

    for entry in users_data:
        if entry['userId'] == focus_user_id:
            # Ensure time zones are consistent for this calculation
            day_difference = (current_time - datetime.fromisoformat(entry['lastSeenDate'])).days
            if 0 <= day_difference < DAYS_IN_WEEK:
                daily_seconds[day_difference] += 1
                total_seconds += 1

    average_daily_time = sum(daily_seconds) / DAYS_IN_WEEK
    average_weekly_time = total_seconds
    return average_daily_time, average_weekly_time, daily_seconds, total_seconds

# Functions from report_feature branch
# ...

def compute_user_metrics(focus_user_id, metrics, date_from=None, date_to=None):
    average_daily, average_weekly, daily_seconds, total_seconds = averageUserTime(focus_user_id)
    metric_data = {}
    if "dailyAverage" in metrics:
        metric_data["dailyAverage"] = average_daily
    if "weeklyAverage" in metrics:
        metric_data["weeklyAverage"] = average_weekly
    if "total" in metrics:
        metric_data["total"] = total_seconds
    if "min" in metrics:
        metric_data["min"] = min(daily_seconds)
    if "max" in metrics:
        metric_data["max"] = max(daily_seconds)
    return metric_data

# More functions from report_feature branch

def generate_report(report_name, metrics, users, date_from=None, date_to=None):
    report = {}
    for user_id in users:
        try:
            report[user_id] = compute_user_metrics_from_csv(user_id, metrics, "dataset.csv", date_from, date_to)
        except Exception as e:
            report[user_id] = {"error": str(e)}

    all_reports[report_name] = report
    return report

def get_report(report_name, date_from=None, date_to=None):
    report = all_reports.get(report_name, {})
    if date_from and date_to:
        filtered_report = {}
        for user_id, data in report.items():
            user_data = {}
            for metric, value in data.items():
                if metric in ["dailyAverage", "weeklyAverage"]:
                    user_data[metric] = value
                elif metric in ["total", "min", "max"]:
                    avg_daily, avg_weekly, daily_seconds, total_seconds = averageUserTime(user_id)
                    if metric == "total":
                        user_data["total"] = total_seconds
                    elif metric == "min":
                        user_data["min"] = min(daily_seconds)
                    elif metric == "max":
                        user_data["max"] = max(daily_seconds)
            filtered_report[user_id] = user_data
        return filtered_report
    return report
