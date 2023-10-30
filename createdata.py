import csv
import requests
import sys
import logging
from api_utils import collect_api_data

# Configure basic logger
logging.basicConfig(level=logging.INFO)


def save_data_to_csv(data, filename="dataset.csv"):
    try:
        with open(filename, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Check if data is not empty and is a list of dicts
            if data and isinstance(data, list) and all(isinstance(item, dict) for item in data):
                headers = data[0].keys()
                writer.writerow(headers)

                for item in data:
                    writer.writerow(item.values())
            else:
                logging.warning("No data to write or data format is incorrect.")
    except Exception as e:
        logging.error(f"Error while writing data to CSV: {e}")
        raise

if __name__ == "__main__":
    # Optionally take filename from command line
    filename = sys.argv[1] if len(sys.argv) > 1 else "dataset.csv"

    try:
        logging.info("Starting data collection...")
        data = collect_api_data(delay_seconds=1, max_iterations=100)
        logging.info("Data collection completed. Saving to CSV...")
        save_data_to_csv(data, filename)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
