import requests


def get_simulation_results(bearer_token, tenant_id, api_base_url, scenario_id):
    url = f'{api_base_url}scenario/{scenario_id}'
    payload = {}
    headers = {
        'x-tenant-id': tenant_id,  # SPA tenant-id
        'Authorization': bearer_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)