import json
import requests


def post_simulation_request(bearer_token_input, payload_input, tenant_id, api_base_url):
    payload = json.dumps(payload_input)

    headers = {
        'x-tenant-id': tenant_id,
        'Authorization': bearer_token_input,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", api_base_url + 'submit', headers=headers, data=payload)

    print("Response :" + response.text)
    scenario_id = response.json().get('data').get('run_ids')[0]
    print(f"simulation {scenario_id} running..")
    return scenario_id
