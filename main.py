from time_utils import humanize_time_difference
from api_utils import fetch_users_last_seen

offset = 0

while True:

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
