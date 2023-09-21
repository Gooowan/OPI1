import requests
from datetime import datetime, timedelta

import re


def humanize_time_difference(last_seen_date):
    """Humanize the time difference between the given date and now.

    Args:
        last_seen_date: A string representing the date to be humanized. The
            date must be in the format `YYYY-MM-DDTHH:MM:SS` or
            `YYYY-MM-DDTHH:MM:SS.f`.

    Returns:
        A string representing the humanized time difference, such as "a moment
        ago", "an hour ago", or "more than a week ago".
    """

    if not last_seen_date:
        return "Unknown"

    now = datetime.utcnow()

    # Match the date and fractional seconds using a regular expression.
    match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d+)?", last_seen_date)
    if not match:
        return "Unknown time format"

    # Convert the date string to a datetime object.
    date_time = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")

    # Calculate the time difference between now and the given date.
    difference = now - date_time

    # Use the time difference to determine the humanized description.
    if difference < timedelta(minutes=1):
        return "online"
    elif difference < timedelta(minutes=10):
        return "recently"
    elif difference < timedelta(hours=1):
        return "an hour ago"
    elif difference < timedelta(days=1):
        return "a day ago"
    elif difference < timedelta(days=7):
        return "a week ago"
    else:
        return "more than a week ago"


offset = 0

while True:
    count = 0
    response = requests.get(f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}",
                            headers={'accept': 'application/json'})

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data
        response_data = response.json()

        # Check if the JSON data is empty
        if not response_data['data']:
            break

        # Iterate over the user data and print userId and humanized lastSeenDate
        for user_info in response_data['data']:
            user_id = user_info['userId']

            # Check if the lastSeenDate key exists
            if 'lastSeenDate' in user_info:
                last_seen_description = humanize_time_difference(user_info['lastSeenDate'])
                print(f"{user_id} {last_seen_description}")
                count += 1

        # Increment the offset
        offset += count
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        break
