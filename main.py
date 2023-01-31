import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

BASE_URL = "https://api.cloudflare.com/client/v4/"

API_TOKEN = os.environ['API_TOKEN']
ZONE_ID = os.environ['ZONE_ID']
DOMAINS_TO_UPDATE = os.environ['DOMAINS_TO_UPDATE'].split(",")


def list_dns_records(zone_id: str,
                     api_token: str) -> dict:
    url = f"{BASE_URL}zones/{zone_id}/dns_records"
    print(url)
    response = requests.get(url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    })

    return response.json()


def filter_records(dns_records: dict,
                   domains: list[str],
                   record_type: str) -> list[dict]:
    filtered = [item for item in dns_records["result"] if item["name"] in domains and item["type"] == record_type]
    return filtered


def update_dns_record(zone_id: str,
                      api_token: str,
                      record: dict) -> dict:
    url = f"{BASE_URL}zones/{zone_id}/dns_records/{record['id']}"
    print(url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.put(url,
                            headers=headers,
                            json=record,
                            )

    return response.json()


def main():
    records = list_dns_records(zone_id=ZONE_ID, api_token=API_TOKEN)
    # print(json.dumps(records, indent=2))
    filtered_records = filter_records(dns_records=records, domains=DOMAINS_TO_UPDATE, record_type="A")
    # print(json.dumps(filtered_records, indent=2))

    for r in filtered_records:
        r["content"] = "1.1.1.1"
        r["comment"] = "updated automatically by konso's updater script"
        del r["created_on"]
        del r["modified_on"]

    print(json.dumps(filtered_records, indent=2))

    for r in filtered_records:
        update_dns_record(zone_id=ZONE_ID,
                          api_token=API_TOKEN,
                          record=r)




if __name__ == '__main__':
    main()
