import requests
from datetime import datetime, timedelta
import re

translations = {
    'en': {
        'just_now': "is online just now",
        'less_minute': "was online less than a minute ago",
        'couple_minutes': "was online a couple of minutes ago",
        'hour_ago': "was online an hour ago",
        'today': "was online today",
        'yesterday': "was online yesterday",
        'this_week': "was online this week",
        'long_time_ago': "was online a long time ago",
        'unknown': "Unknown",
        'unknown_format': "Unknown time format"
    },
    'ua': {
        'just_now': "зараз в мережі",
        'less_minute': "був в мережі менше хвилини тому",
        'couple_minutes': "був в мережі кілька хвилин тому",
        'hour_ago': "був в мережі годину тому",
        'today': "був в мережі сьогодні",
        'yesterday': "був в мережі вчора",
        'this_week': "був в мережі на цьому тижні",
        'long_time_ago': "був в мережі давно",
        'unknown': "Невідомо",
        'unknown_format': "Невідомий формат часу"
    }
}

def humanize_time_difference(last_seen_date, lang='en'):
    if not last_seen_date:
        return translations[lang]['unknown']

    now = datetime.utcnow()

    # Match the date and fractional seconds using a regular expression.
    match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d+)?", last_seen_date)
    if not match:
        return translations[lang]['unknown_format']

    # Convert the date string to a datetime object.
    date_time = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")

    # Calculate the time difference between now and the given date.
    difference = now - date_time

    # Use the time difference to determine the humanized description.
    if difference < timedelta(seconds=30):
        return translations[lang]['just_now']
    elif difference < timedelta(seconds=60):
        return translations[lang]['less_minute']
    elif difference < timedelta(minutes=59):
        return translations[lang]['couple_minutes']
    elif difference < timedelta(minutes=119):
        return translations[lang]['hour_ago']
    elif difference < timedelta(hours=24) and difference.total_seconds() >= 7200:
        return translations[lang]['today']
    elif difference < timedelta(days=1):
        return translations[lang]['yesterday']
    elif difference < timedelta(days=7):
        return translations[lang]['this_week']
    else:
        return translations[lang]['long_time_ago']

offset = 0

while True:
    count = 0
    response = requests.get(f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}",
                            headers={'accept': 'application/json'})

    lang = input("Enter your language, виберіть мову: en, ua: ")
    if lang != 'ua' and lang != 'en':
        lang = "en"

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data
        response_data = response.json()

        # Check if the JSON data is empty
        if not response_data['data']:
            break

        # Iterate over the user data and print userId and humanized lastSeenDate
        for user_info in response_data['data']:
            user_nickname = user_info['nickname']

            # Check if the lastSeenDate key exists
            if 'lastSeenDate' in user_info:
                last_seen_description = humanize_time_difference(user_info['lastSeenDate'], lang)
                print(f"{user_nickname} {last_seen_description}")
                count += 1

        # Increment the offset
        offset += count
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        break
