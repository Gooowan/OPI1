import requests
from time import sleep
from datetime import datetime


def fetch_users_last_seen(offset=0):
    response = requests.get(f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}",
                            headers={'accept': 'application/json'})
    return response


def collect_api_data(delay_seconds=10, max_iterations=None):
    """
    Continuously polls the API using fetch_users_last_seen and collects its data with a specified delay.

    Args:
    - delay_seconds (int): Time delay between consecutive API requests.
    - max_iterations (int): Maximum number of times the API will be polled. If None, it will run indefinitely.

    Returns:
    - list: A list of collected data from the API.
    """
    collected_data = []
    iterations = 0

    while max_iterations is None or iterations < max_iterations:
        try:
            offset = len(collected_data)
            response = fetch_users_last_seen(offset)

            if response.status_code == 200:
                data = response.json()
                collected_data.extend(data['data'])  # Assuming the API returns a 'data' key with a list of user data.
                # print(f"Collected {len(data['data'])} data entries.")
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error occurred: {e}")

        # Sleep for the specified delay before the next request
        sleep(delay_seconds)

        iterations += 1

    return collected_data

# Example usage:
# data = collect_api_data(delay_seconds=10, max_iterations=5)


def predict_online_chance(user_id, specified_date, user_last_seen_data):
    """Predicts the chance that a user will be online on a specified date.
    
    Args:
        user_id (int): The ID of the user.
        specified_date (datetime): The date for which to make the prediction.
        user_last_seen_data (dict): Historical data of user's last seen dates.
        
    Returns:
        float: The probability (from 0 to 1) that the user will be online on the specified date.
    """
    
    if user_id not in user_last_seen_data:
        return 0.0  # If no historical data for the user
    
    # Extracting weekday and time from the specified date
    specified_weekday = specified_date.weekday()
    specified_time = specified_date.time()

    # Counting occurrences when the user was online at the same weekday and time
    occurrences = sum(1 for date in user_last_seen_data[user_id]
                      if date.weekday() == specified_weekday and date.time() == specified_time)
    
    total_weeks = len(set([date.date() for date in user_last_seen_data[user_id]])) / 7.0
    
    # Calculating the probability
    chance = occurrences / total_weeks
    
    return chance


def online_prediction(specified_date, users_data):
    """Predicts the average number of users online on a specified date based on historical data.
    
    Args:
        specified_date (datetime): The date for which to make the prediction.
        users_data (list): List of dictionaries containing user data with 'lastSeenDate' key.
        
    Returns:
        float: The predicted average number of users online at the specified date.
    """
    
    # Extracting weekday and time from the specified date
    specified_weekday = specified_date.weekday()
    specified_time = specified_date.time()

    # Counting occurrences of users online at the same weekday and time
    occurrences = [entry for entry in users_data if 
                   datetime.fromisoformat(entry['lastSeenDate']).weekday() == specified_weekday and 
                   datetime.fromisoformat(entry['lastSeenDate']).time() == specified_time]
    
    # Calculating the average number of users online
    average_users_online = len(occurrences) / len(users_data)
    
    return average_users_online
