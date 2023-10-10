from time_utils import humanize_time_difference
from api_utils import fetch_users_last_seen, collect_api_data
from translations import translations  # Assuming you have this import in your actual code.
from datetime import datetime

# ya v dzhakuzi, eto fact
users_data = collect_api_data(delay_seconds=1, max_iterations=5)

user_last_seen_data = {}
for entry in users_data:
    user_id = entry['userId']
    if user_id not in user_last_seen_data:
        user_last_seen_data[user_id] = []
    user_last_seen_data[user_id].append(entry['lastSeenDate'])


def usersOnline():
    user_data = collect_api_data(delay_seconds=10, max_iterations=5)

    online_count = 0
    for user_info_f in user_data:
        status = humanize_time_difference(user_info_f.get('lastSeenDate', None), lang)
        if status in [translations[lang]['online']]:
            online_count += 1

    print(f"There are {online_count} users online right now.")
    return online_count


def nearestOnlineTime(date, user_id):

    if user_id not in user_last_seen_data:
        return {"error": "User not found"}, 404

    online_times = user_last_seen_data[user_id]

    wasUserOnline = None if date not in online_times else (True if date in online_times else False)

    nearestOnlineTime = None
    if not wasUserOnline:

        nearestOnlineTime = min(online_times, key=lambda d: abs(
            datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")))

    return {
        "wasUserOnline": wasUserOnline,
        "nearestOnlineTime": nearestOnlineTime
    }


def onlinePrediction(date):

    predict_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    day_of_week = predict_datetime.weekday()
    time_of_day = predict_datetime.time()

    online_counts = {i: {} for i in range(7)}

    for user_id, timestamps in user_last_seen_data.items():
        for timestamp in timestamps:
            timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            if timestamp_datetime.time() == time_of_day:
                online_counts[timestamp_datetime.weekday()][time_of_day] = online_counts[
                                                                               timestamp_datetime.weekday()].get(
                    time_of_day, 0) + 1

    total_users = online_counts[day_of_week].get(time_of_day, 0)
    avg_users = total_users / len(user_last_seen_data)
    return avg_users


def userPrediction(date, user_id):

    if user_id not in user_last_seen_data:
        return {"error": "User not found"}, 404

    predict_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    day_of_week = predict_datetime.weekday()
    time_of_day = predict_datetime.time()

    user_timestamps = user_last_seen_data[user_id]
    matching_dates = [timestamp for timestamp in user_timestamps if datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").weekday() == day_of_week and datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").time() == time_of_day]

    weeks_in_data = len(set([datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").date().isocalendar()[1] for timestamp in user_timestamps]))
    probability = len(matching_dates) / weeks_in_data if weeks_in_data > 0 else 0

    return {"probability": probability}


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

                print(f"Online users: {usersOnline()}")

            elif input_command == '2':

                date = input("Date. Input format - 2023-27-09T20:00:00: ")
                user_id = input("Date. A4DC2287-B03D-430C-92E8-02216D828709: ")

                print(nearestOnlineTime(date, user_id))
            elif input_command == '3':

                date = input("Input time in format: 2023-10-10T20:00:00: ")
                print(f"Predicted number of users online: {onlinePrediction(date)}")

            elif input_command == '4':
                date = input("Date. Input format - 2023-27-09T20:00:00: ")
                user_id = input("Date. A4DC2287-B03D-430C-92E8-02216D828709: ")

                print(userPrediction(date, user_id))
            elif input_command == 'exit':
                break
            else:
                print("Invalid feature choice. Try again.")
