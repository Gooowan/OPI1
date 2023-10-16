import csv
import requests
from api_utils import collect_api_data


def save_data_to_csv(data, filename="dataset.csv"):
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        headers = data[0].keys()
        writer.writerow(headers)

        for item in data:
            writer.writerow(item.values())


if __name__ == "__main__":
    data = collect_api_data(delay_seconds=1, max_iterations=100)
    save_data_to_csv(data)
