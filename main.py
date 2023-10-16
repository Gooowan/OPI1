from time_utils import humanize_time_difference
from api_utils import  collect_api_data #, fetch_users_last_seen
from translations import translations  # Assuming you have this import in your actual code.
from datetime import datetime, timedelta
import csv


def load_data_from_csv(filename="dataset.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


# ya v dzhakuzi, eto fact
users_data = load_data_from_csv()

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


def userPrediction(date, user_id, tolerance):

    if user_id not in user_last_seen_data:
        return {"error": "User not found"}, 404

    predict_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    day_of_week = predict_datetime.weekday()
    time_of_day = predict_datetime.time()

    user_timestamps = user_last_seen_data[user_id]
    matching_dates = [timestamp for timestamp in user_timestamps if datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").weekday() == day_of_week and datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").time() == time_of_day]

    weeks_in_data = len(set([datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").date().isocalendar()[1] for timestamp in user_timestamps]))
    probability = len(matching_dates) / weeks_in_data if weeks_in_data > 0 else 0

    if tolerance <= probability:
        return {"True. probability": probability}
    else:
        return {"False. probability": probability}


def totalUserMinutes(focus_user_id):
    secCollect = 5
    users_data = collect_api_data(delay_seconds=1, max_iterations=secCollect)
    total_seconds = 0

    current_time = datetime.utcnow()

    for entry in users_data:

        if entry['userId'] == focus_user_id and current_time - datetime.fromisoformat(entry['lastSeenDate']) <= timedelta(minutes=1):
            total_seconds += 1

    return total_seconds


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

    return average_daily_time, average_weekly_time


while True:
    offset = 0
    lang = input("Enter your language, виберіть мову: en, ua: ")

    if lang not in ['ua', 'en']:
        lang = "en"

    # while True:
    #     count = 0
    #     response = fetch_users_last_seen(offset)
    #
    #
    #     if response.status_code == 200:
    #         response_data = response.json()
    #         if not response_data['data']:
    #             break
    #
    #         for user_info in response_data['data']:
    #             user_nickname = user_info.get('nickname', '')
    #             last_seen_description = humanize_time_difference(user_info.get('lastSeenDate', None), lang)
    #             print(f"{user_nickname} {last_seen_description}")
    #             count += 1
    #
    #         offset += count
    #     else:
    #         print(f"Failed to fetch data. Status code: {response.status_code}")
    #         break

    while True:
        input_command = input("Input your feature (1/2/3/4/5/6/7 or 'exit' to quit): ")

        if input_command == '1':

            print(f"Online users: {usersOnline()}")

        elif input_command == '2':

            date = input("Date. Input format - 2023-27-09T20:00:00: ")
            user_id = input("User ID: A4DC2287-B03D-430C-92E8-02216D828709: ")

            print(nearestOnlineTime(date, user_id))

        elif input_command == '3':

            date = input("Input time in format: 2023-10-10T20:00:00: ")
            print(f"Predicted number of users online: {onlinePrediction(date)}")

        elif input_command == '4':
            date = input("Date. Input format - 2023-27-09T20:00:00: ")
            user_id = input("User ID: A4DC2287-B03D-430C-92E8-02216D828709: ")
            tolarance = input("Input tolerance in format, 0,82:  ")

            print(userPrediction(date, user_id, tolarance))

        elif input_command == '5':
            user_id = input("User ID: A4DC2287-B03D-430C-92E8-02216D828709: ")
            print(totalUserMinutes(user_id))

        elif input_command == '6':
            user_id = input("User ID: A4DC2287-B03D-430C-92E8-02216D828709: ")
            daily_avg, weekly_avg = averageUserTime(user_id)
            print(f"For user {user_id}:\n"
                  f"Average daily active time: {daily_avg:.0f} seconds\n"
                  f"Average weekly active time: {weekly_avg:.0f} seconds")

        elif input_command == '7':
            user_id = input("Enter User ID to delete all their data (GDPR compliance): ")
            if user_id in user_last_seen_data:
                del user_last_seen_data[user_id]
                print(f"All data related to user {user_id} has been deleted!")
            else:
                print("User ID not found.")
        elif input_command == 'exit':
            break

        else:
            print("Invalid feature choice. Try again.")
