from datetime import datetime

import pandas as pd

from api_utils import collect_api_data

dataset_df = pd.read_csv("dataset.csv")

def averageUserTime(focus_user_id):

    users_data = collect_api_data(delay_seconds=1,
                                  max_iterations=7 * 24 * 60 * 60)

    daily_seconds = [0 for _ in range(7)]
    total_seconds = 0

    current_time = datetime.utcnow()

    for entry in users_data:
        if entry['userId'] == focus_user_id:
            day_difference = (current_time - datetime.fromisoformat(entry['lastSeenDate'])).days
            if 0 <= day_difference < 7:
                daily_seconds[day_difference] += 1
                total_seconds += 1

    average_daily_time = sum(daily_seconds) / 7
    average_weekly_time = total_seconds

    return average_daily_time, average_weekly_time, daily_seconds, total_seconds

def compute_user_metrics(focus_user_id, metrics, date_from, date_to):
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


def generate_report(report_name, metrics, users, date_from, date_to):
    report = {}
    for user_id in users:
        report[user_id] = compute_user_metrics(user_id, metrics, date_from, date_to)

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
                    avg_daily, avg_weekly, daily_seconds, total_seconds = averageUserTime(user_id, date_from, date_to)
                    if metric == "total":
                        user_data["total"] = total_seconds
                    elif metric == "min":
                        user_data["min"] = min(daily_seconds)
                    elif metric == "max":
                        user_data["max"] = max(daily_seconds)
            filtered_report[user_id] = user_data
        return filtered_report
    return report


all_reports = {}
