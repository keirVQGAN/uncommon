
import yaml
import requests
import json

def unstable(config_file: str) -> dict:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    url = config['url']
    payload = json.dumps(config['payload'])
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()
    