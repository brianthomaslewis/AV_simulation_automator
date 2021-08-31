import json
import time
import requests


def get_kpi_results(bearer_token_input, api_base_url, tenant_id, scenario_id,
                    output_json_fp):
    print("Retrieving scenario: %s ..." % scenario_id)
    url = f'{api_base_url}summary/{scenario_id}/kpi'
    url_info = f'{api_base_url}scenario/{scenario_id}'
    payload = {}
    headers = {
        'x-tenant-id': tenant_id,
        'Authorization': bearer_token_input
    }

    info_response = requests.request("GET", url_info, headers=headers, data=payload)
    run_json = json.loads(info_response.text)['data']['simulationRun']['status']['state']

    # Check to see if there is actual output
    output = 0

    if run_json == 'EXECUTING' or run_json == 'COMPLETED':
        while run_json == 'EXECUTING':
            print('Simulations still running. Sleeping for 30 seconds until next attempted "GET" call...')
            time.sleep(30)
            info_response = requests.request("GET", url_info, headers=headers, data=payload)
            run_json = json.loads(info_response.text)['data']['simulationRun']['status']['state']
        response = requests.request("GET", url, headers=headers, data=payload)
        fil = open(output_json_fp, "w")
        fil.write(response.text)
        fil.close()
        output += 1

    return output


def get_scenario_map(output_hash_fp):
    with open(output_hash_fp) as f:
        data = json.load(f)
    return data
