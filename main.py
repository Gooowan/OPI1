from time_utils import humanize_time_difference
from api_utils import fetch_users_last_seen, collect_api_data
from translations import translations  # Assuming you have this import in your actual code.
from datetime import datetime


# Assuming the collected data is stored in this variable
users_data = collect_api_data(delay_seconds=0, max_iterations=5)

# Convert the collected data to a more usable format
user_last_seen_data = {}
for entry in users_data:
    user_id = entry['userId']
    if user_id not in user_last_seen_data:
        user_last_seen_data[user_id] = []
    user_last_seen_data[user_id].append(entry['lastSeenDate'])

def feature1(lang='en'):
    # Fetch latest user data
    user_data = collect_api_data(delay_seconds=10, max_iterations=5)  # Adjust parameters as needed

    online_count = 0
    for user_info in user_data:
        status = humanize_time_difference(user_info.get('lastSeenDate', None), lang)
        if status in [translations[lang]['online']]:
            online_count += 1

    print(f"There are {online_count} users online right now.")
    return online_count


def feature2(date, user_id):
    # Check if user exists
    if user_id not in user_last_seen_data:
        return {"error": "User not found"}, 404

    online_times = user_last_seen_data[user_id]

    # If we don't have data for the specific date, set wasUserOnline to None
    wasUserOnline = None if date not in online_times else (True if date in online_times else False)

    nearestOnlineTime = None
    if not wasUserOnline:
        # Find nearest online time
        nearestOnlineTime = min(online_times, key=lambda d: abs(
            datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")))

    return {
        "wasUserOnline": wasUserOnline,
        "nearestOnlineTime": nearestOnlineTime
    }


def feature3(response_data):
    pass


def feature4(response_data):
    pass


while True:
    offset = 0
    lang = input("Enter your language, виберіть мову: en, ua: ")

    if lang not in ['ua', 'en']:
        lang = "en"

    while True:
        count = 0
        response = fetch_users_last_seen(offset)

        if response.status_code == 200:
            response_data = response.json()
            if not response_data['data']:
                break

            for user_info in response_data['data']:
                user_nickname = user_info.get('nickname', '')
                last_seen_description = humanize_time_difference(user_info.get('lastSeenDate', None), lang)
                print(f"{user_nickname} {last_seen_description}")
                count += 1

            offset += count
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

        while True:
            input_command = input("Input your feature (1/2/3/4 or 'exit' to quit): ")

            if input_command == '1':
                print(f"Online users: {feature1(lang)}")
            elif input_command == '2':
                date = "2023-27-09T20:00:00"
                user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
                print(feature2(date, user_id))
            elif input_command == '3':
                feature3(response_data)
            elif input_command == '4':
                feature4(response_data)
            elif input_command == 'exit':
                break
            else:
                print("Invalid feature choice. Try again.")
