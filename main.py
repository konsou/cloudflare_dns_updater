import json
import os
from copy import deepcopy

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
    print(f"Getting list of current records...")
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
    print(f"updating {record['name']} {record['type']} record with content {record['content']}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.put(url,
                            headers=headers,
                            json=record,
                            )

    return response.json()


def update_multiple_dns_records(zone_id: str,
                                api_token: str,
                                records: list[dict]) -> list[dict]:
    results = []
    for r in records:
        result = update_dns_record(zone_id=zone_id,
                                   api_token=api_token,
                                   record=r)
        results.append(result)
    return results


def get_external_ip() -> str:
    ip = requests.get('https://api.ipify.org').text
    return ip


def update_records(records: list[dict],
                   new_ip: str) -> list[dict]:
    updated_records = []
    for r in records:
        if r["content"] == new_ip:
            print(f"Skip {r['name']} - address not changed")
            continue
        r_copy = deepcopy(r)
        r_copy["content"] = new_ip
        r_copy["comment"] = "updated automatically by konso's updater script"
        del r_copy["created_on"]
        del r_copy["modified_on"]
        updated_records.append(r_copy)
    return updated_records


def main():
    records = list_dns_records(zone_id=ZONE_ID, api_token=API_TOKEN)
    filtered_records = filter_records(dns_records=records, domains=DOMAINS_TO_UPDATE, record_type="A")
    external_ip = get_external_ip()
    print(f"External IP is {external_ip}")
    updated_records = update_records(filtered_records, new_ip=external_ip)

    if updated_records:
        update_multiple_dns_records(zone_id=ZONE_ID,
                                    api_token=API_TOKEN,
                                    records=updated_records)

if __name__ == '__main__':
    main()
