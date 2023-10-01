import re
from datetime import datetime, timedelta
from translations import translations

def humanize_time_difference(last_seen_date, lang='en'):
    if not last_seen_date:
        return translations[lang]['unknown']

    now = datetime.utcnow()

    match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d+)?", last_seen_date)
    if not match:
        return translations[lang]['unknown_format']

    date_time = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
    difference = now - date_time

    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_yesterday = start_of_today - timedelta(days=1)

    if difference < timedelta(seconds=30):
        return translations[lang]['just_now']
    elif difference < timedelta(seconds=60):
        return translations[lang]['less_minute']
    elif difference < timedelta(minutes=59):
        return translations[lang]['couple_minutes']
    elif difference < timedelta(minutes=119):
        return translations[lang]['hour_ago']
    elif date_time >= start_of_today:
        return translations[lang]['today']
    elif start_of_yesterday + timedelta(hours=2) <= date_time < start_of_today:
        return translations[lang]['yesterday']
    elif difference < timedelta(days=7):
        return translations[lang]['this_week']
    else:
        return translations[lang]['long_time_ago']
