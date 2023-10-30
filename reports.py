
from datetime import datetime
import pandas as pd
from api_utils import collect_api_data
import csv

# Global variable to store all reports
all_reports = {}

# Constants
DAYS_IN_WEEK = 7

dataset_df = pd.read_csv("dataset.csv")


from datetime import datetime
import pandas as pd

from datetime import datetime
import pandas as pd


def adjusted_averageUserTime_within_range(focus_user_id, filename='dataset.csv', date_from=None, date_to=None):
    # Read data from the specified CSV file
    df = pd.read_csv(filename)

    # Converting 'lastSeenDate' to datetime, considering NaNs and timezone
    df['lastSeenDate'] = pd.to_datetime(df['lastSeenDate'], errors='coerce', utc=True)

    # Filter data based on date_from and date_to if provided
    if date_from is not None:
        df = df[df['lastSeenDate'] >= pd.to_datetime(date_from, utc=True)]
    if date_to is not None:
        df = df[df['lastSeenDate'] <= pd.to_datetime(date_to, utc=True)]

    # Initialize variables to calculate total time and count of days
    total_time = 0
    days = 0
    daily_seconds = []

    # Iterate over each row to calculate the total time and days
    for index, row in df.iterrows():
        if row['userId'] == focus_user_id and pd.notna(row['lastSeenDate']):
            seconds_spent = (datetime.utcnow().replace(tzinfo=pd.Timestamp.utcnow().tz) - row[
                'lastSeenDate']).total_seconds()
            total_time += seconds_spent
            days += 1
            daily_seconds.append(seconds_spent)

    # Handle the case where days is zero to avoid division by zero
    average_daily = total_time / days if days != 0 else 0
    average_weekly = average_daily * 7
    total_seconds = total_time

    # Return a dictionary with the calculated metrics
    return average_daily, average_weekly, daily_seconds, total_seconds


def adjusted_averageUserTime(focus_user_id, filename='dataset.csv'):
    import pandas as pd
    from datetime import datetime

    # Read data from the specified CSV file within the function
    df = pd.read_csv(filename)
    df['lastSeenDate'] = pd.to_datetime(df['lastSeenDate'])

    total_time = 0
    days = 0
    for index, row in df.iterrows():
        if row['userId'] == focus_user_id:
            #total_time += (datetime.utcnow() - row['lastSeenDate']).seconds
            days += 1

    # Handle the case where days is zero
    average_daily = total_time / days if days != 0 else 0
    average_weekly = average_daily * 7

    return {focus_user_id: {"average_daily": average_daily, "average_weekly": average_weekly}}


def compute_user_metrics(focus_user_id, metrics, date_from=None, date_to=None):
    average_daily, average_weekly, daily_seconds, total_seconds = adjusted_averageUserTime_within_range(
        focus_user_id, date_from=date_from, date_to=date_to
    )
    # average_daily, average_weekly, daily_seconds, total_seconds = adjusted_averageUserTime(focus_user_id)
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


def read_csv_data(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


def averageUserTime_from_csv(focus_user_id, csv_data):
    user_times = [int(row['timeSpentSeconds']) for row in csv_data if int(row['userId']) == focus_user_id]
    total_seconds = sum(user_times)
    daily_seconds = user_times  # Assuming each record corresponds to a day
    average_daily = total_seconds / len(daily_seconds)
    average_weekly = 7 * average_daily
    return average_daily, average_weekly, daily_seconds, total_seconds


def compute_user_metrics_from_csv(focus_user_id, metrics, filename, date_from=None, date_to=None):
    csv_data = read_csv_data(filename)

    # Filter data based on date range if provided
    if date_from or date_to:
        csv_data = [
            row for row in csv_data
            if (not date_from or datetime.strptime(row['date'], '%Y-%m-%d').date() >= date_from) and
               (not date_to or datetime.strptime(row['date'], '%Y-%m-%d').date() <= date_to)
        ]

    average_daily, average_weekly, daily_seconds, total_seconds = averageUserTime_from_csv(focus_user_id, csv_data)

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


def generate_report(report_name, metrics, users, date_from=None, date_to=None):
    report = {}
    for user_id in users:
        try:
            # report[user_id] = compute_user_metrics_from_csv(user_id, metrics, "dataset.csv", date_from, date_to)
            report[user_id] = compute_user_metrics(user_id, metrics, date_from, date_to)
        except Exception as e:
            report[user_id] = {"error": e}
    
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
                    avg_daily, avg_weekly, daily_seconds, total_seconds = adjusted_averageUserTime(user_id)
                    if metric == "total":
                        user_data["total"] = total_seconds
                    elif metric == "min":
                        user_data["min"] = min(daily_seconds)
                    elif metric == "max":
                        user_data["max"] = max(daily_seconds)
            filtered_report[user_id] = user_data
        return filtered_report
    return report
