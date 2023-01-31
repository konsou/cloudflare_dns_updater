import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

BASE_URL = "https://api.cloudflare.com/client/v4/"

API_TOKEN = os.environ['API_TOKEN']
ZONE_ID = os.environ['ZONE_ID']


def list_dns_records() -> dict:
    url = f"{BASE_URL}zones/{ZONE_ID}/dns_records"
    print(url)
    response = requests.get(url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    })

    return response.json()


def main():
    records = list_dns_records()
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
