import requests


def fetch_users_last_seen(offset=0):
    response = requests.get(f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}",
                            headers={'accept': 'application/json'})
    return response


def fetch_online_users(offset=0):

    # Define the base URL for the API
    base_url = "https://sef.podkolzin.consulting/api/stats/users"

    # Define the date parameter
    date_param = "2023-27-09-20:00"  # Update with your desired date and time

    # Create the full URL with the date parameter
    url = f"{base_url}?date={date_param}"

    try:
        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and print the response JSON
            data = response.json()
            print("Users Online:", data.get("usersOnline"))
        else:
            print("Request failed with status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", str(e))

