import requests


def fetch_users_last_seen(offset=0):
    response = requests.get(f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}",
                            headers={'accept': 'application/json'})
    return response
