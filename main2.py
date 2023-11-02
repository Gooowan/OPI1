from flask import Flask, request, jsonify
app = Flask(__name__)

import os
from dateutil import parser
from time_utils import humanize_time_difference
from api_utils import collect_api_data, fetch_users_last_seen  # , fetch_users_last_seen
from translations import translations
from datetime import datetime, timedelta
from reports import generate_report, get_report, adjusted_averageUserTime

import csv

# Global list to store the IDs of users whose data has been deleted (GDPR compliance)
User_forgotten = []

# File path for storing forgotten users' IDs
forgotten_users_file = "forgotten_users.txt"


def load_forgotten_users():
    if not os.path.exists(forgotten_users_file):
        return []

    with open(forgotten_users_file, "r") as file:
        return file.read().splitlines()


def save_forgotten_users():
    if not User_forgotten:
        return "Nothing to save"
    with open(forgotten_users_file, "a") as file:
        for user_id in User_forgotten:
            file.write(user_id + '\n')


# Load forgotten users into the User_forgotten list during initialization
User_forgotten.extend(load_forgotten_users())


def load_data_from_csv(filename="dataset.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader if row['userId'] not in User_forgotten]
    return data


def delete_forgotten_users_from_csv(filename="dataset.csv"):
    demo_data = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['userId'] not in User_forgotten:
                demo_data.append(row)


    with open(filename, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(demo_data)

    print(f"Data for forgotten users has been deleted from {filename}")


users_data = load_data_from_csv()

user_last_seen_data = {}
for entry in users_data:
    user_id = entry['userId']
    if user_id not in user_last_seen_data:
        user_last_seen_data[user_id] = []
    user_last_seen_data[user_id].append(entry['lastSeenDate'])


def usersOnline():
    user_data = collect_api_data(delay_seconds=0, max_iterations=5)

    online_count = 0
    for user_info_f in user_data:
        status = humanize_time_difference(user_info_f.get('lastSeenDate', None))
        if status in [translations['en']['online']]:
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


def gdpr_compliance(user_id):
    if user_id in user_last_seen_data:
        del user_last_seen_data[user_id]
        User_forgotten.append(user_id)
        delete_forgotten_users_from_csv()
        return {"message": f"All data related to user {user_id} has been deleted!"}
    else:
        return {"error": "User ID not found."}



@app.route('/users_online')
def route_users_online():
    return jsonify(usersOnline())

@app.route('/nearest_online_time')
def route_nearest_online_time():
    date = request.args.get("date")
    user_id = request.args.get("user_id")
    return jsonify(nearestOnlineTime(date, user_id))

@app.route('/online_prediction')
def route_online_prediction():
    date = request.args.get("date")
    return jsonify(onlinePrediction(date))

@app.route('/user_prediction')
def route_user_prediction():
    date = request.args.get("date")
    user_id = request.args.get("user_id")
    tolerance = request.args.get("tolerance")
    return jsonify(userPrediction(date, user_id, tolerance))

@app.route('/total_user_minutes')
def route_total_user_minutes():
    user_id = request.args.get("user_id")
    return jsonify(totalUserMinutes(user_id))

@app.route('/adjusted_average_user_time')
def route_adjusted_average_user_time():
    user_id = request.args.get("user_id")
    result = adjusted_averageUserTime(user_id)
    return jsonify({"daily_average": result[0], "weekly_average": result[1]})

@app.route('/gdpr_compliance')
def route_gdpr_compliance():
    user_id = request.args.get("user_id")
    return jsonify(gdpr_compliance(user_id))

from reports import generate_report, get_report


@app.route('/generate_report', methods=['POST'])
def generate_report_endpoint():
    report_name = "Report2"
    metrics = ["dailyAverage", "weeklyAverage", "total", "min", "max"]
    users = ["e13412b2-fe46-7149-6593-e47043f39c91"]

    date_to = "2023-10-26T10:35:02.2858998+00:00"
    date_from = "2000-10-26T13:20:02.2858998+00:00"
    report = generate_report(report_name, metrics, users, date_from, date_to)
    return jsonify(report)


@app.route('/get_report/report_name', methods=['POST'])
def get_report_endpoint(report_name):

    report = "Report2"
    return jsonify(report)


def get_users():
    try:
        all_users = {}
        offset = 0

        for i in range(0, 10):
            response = fetch_users_last_seen(offset)
            if response.status_code == 200:
                response_data = response.json()
                if not response_data['data']:
                    break

                for user in response_data['data']:
                    user_id = user.get("userId", "No userId")
                    nickname = user.get("nickname", "No nickname")
                    last_seen = user.get("lastSeenDate")

                    if last_seen:
                        try:
                            last_seen_date = parser.isoparse(last_seen)
                        except ValueError:
                            continue

                        if user_id not in all_users or last_seen_date < all_users[user_id]["firstOnline"]:
                            all_users[user_id] = {
                                "nickname": nickname,
                                "userId": user_id,
                                "firstOnline": last_seen_date
                            }

                offset += len(response_data['data'])
            else:
                return jsonify({"error": f"Failed to fetch data. Status code: {response.status_code}"}), response.status_code

        for user_id, data in all_users.items():
            data["firstOnline"] = data["firstOnline"].isoformat()

        ordered_data = [
            {
                "nickname": data["nickname"],
                "userId": data["userId"],
                "firstOnline": data["firstOnline"]
            }
            for data in all_users.values()
        ]

        return ordered_data, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/list', methods=['GET'])
def list_users_route():
    data, status_code = get_users()
    return jsonify(data), status_code


if __name__ == '__main__':
    app.run(debug=True)


