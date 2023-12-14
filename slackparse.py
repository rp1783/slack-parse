import json
import csv

# Ask for user input for the JSON file path and CSV file path
json_file_path = input("Enter the path to your JSON file: ")
csv_file_path = input("Enter the path for the CSV output file: ")

def flatten_threads(message, thread_data=None, thread_id=None):
    if thread_data is None:
        thread_data = []

    # Extract the relevant data from the message
    user = message.get("user", "")
    text = message.get("text", "")
    timestamp = message.get("ts", "")  # Use "ts" field for the message timestamp
    thread_ts = message.get("thread_ts", "")

    # Append the message data to the thread_data list along with the thread_id
    thread_data.append({
        "user": user,
        "text": text,
        "timestamp": timestamp,
        "thread_id": thread_ts  # Use "thread_ts" for the thread_id
    })

    # Check if the message has threaded replies
    if "replies" in message:
        for reply in message["replies"]:
            flatten_threads(reply, thread_data, thread_id=thread_ts)

    return thread_data

try:
    # Open and read the JSON file with the appropriate encoding (e.g., UTF-16)
    with open(json_file_path, 'r', encoding='utf-16') as json_file:
        # Parse the JSON data
        messages = json.load(json_file)

        # Specify the CSV column headers, including "thread_id"
        fieldnames = ["user", "text", "timestamp", "thread_id"]

        # Open and write to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write data to the CSV file, including threaded replies and their respective thread_id
            for message in messages:
                thread_data = flatten_threads(message, thread_id=message.get("ts", ""))
                for row in thread_data:
                    writer.writerow(row)

    print(f"CSV data exported to: {csv_file_path}")

except FileNotFoundError:
    print(f"File not found: {json_file_path}")
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
