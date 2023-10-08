import requests
from time import sleep


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
                print(f"Collected {len(data['data'])} data entries.")
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
