import os
import json
import datetime
import requests
import time

def save_and_append(response: dict, output_folder: str) -> None:
    # maximum number of attempts to fetch the result
    max_attempts = 10  
    attempts = 0  

    # Loop until the status is 'success' or maximum number of attempts reached
    while response['status'] != 'success' and attempts < max_attempts:
        time.sleep(response['eta'])  # wait for the estimated time before next fetch
        # Make a request to the fetch_result endpoint to get the updated status
        response = requests.get(response['fetch_result']).json()
        attempts += 1

    # If the status is 'success', proceed with saving the data
    if response['status'] == 'success':
        folder_path = os.path.join(output_folder, str(response['id']))
        i = 0
        while os.path.exists(folder_path):
            i += 1
            folder_path = os.path.join(output_folder, f"{response['id']} ({i})")

        paths = {key: os.path.join(folder_path, f"{response['id']}_{key}.{ext}") 
                 for key, ext in zip(["prompt", "json", "image"], ["txt", "json", "jpg"])}
        os.makedirs(os.path.dirname(paths["prompt"]), exist_ok=True)

        with open(paths["prompt"], 'w') as f:
            f.write(response['meta']['prompt'])

        with open(paths["json"], 'w') as json_f, open(paths["image"], 'wb') as img_f:
            json.dump(response, json_f, indent=4)
            img_f.write(requests.get(response['output'][0]).content)

        try:
            with open('master.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"data": [], "last_updated": ""}

        if not any(item["response"] == response for item in data["data"]):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["data"].append({"response": response, "timestamp": current_time})
            data["last_updated"] = current_time

            with open('master.json', 'w') as f:
                json.dump(data, f, indent=4)
