from time_utils import humanize_time_difference
from api_utils import fetch_users_last_seen


def feature1(response1_data):
    pass


def feature2(response1_data):
    pass


def feature3(response1_data):
    pass


def feature4(response1_data):
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
            input_command = input("Input your feature: ")

            if input_command == 1:
                feature1(response_data)
            elif input_command == 2:
                feature2(response_data)
            elif input_command == 3:
                feature3(response_data)
            else:
                feature4(response_data)

    # while True:
    #     input_command = input("Input your feature: ")
    #
    #     if input_command == 1:
    #         feature1(response_data)
    #     elif input_command == 2:
    #         print("Option 2 selected")
    #     elif input_command == 3:
    #         print("Option 3 selected")
    #     else:
    #         print("Invalid option")
