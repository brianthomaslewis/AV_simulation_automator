# Load modules
import requests
from urllib.parse import urlencode
import time
import yaml

# Import YAML files
with open('config/credentials.yaml') as cred_file:
    creds = yaml.load(cred_file, Loader=yaml.FullLoader)
with open('config/params_paths.yaml') as path_file:
    config_paths = yaml.load(path_file, Loader=yaml.FullLoader)
with open('input_data/params_scenario.yaml') as param_file:
    parameters = yaml.load(param_file, Loader=yaml.FullLoader)

# Set credentials (e.g. "msm_dev", "spa_dev", "spa_stage", "spa_prod")
ciam_creds = 'spa_dev'


def get_CIAM_token():
    query_params = {'client_id': creds['client_ids'][ciam_creds],
                    'client_secret': creds['client_secrets'][ciam_creds],
                    'grant_type': 'client_credentials'}

    query_params = urlencode(query_params, encoding='UTF-8')

    url = f'{config_paths["CIAM_URL"]}?{query_params}'

    headers = {'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, proxies=config_paths['proxy_dict'])

    access_token = response.json().get('access_token')

    if not access_token:
        raise ValueError("Missing access token")

    return access_token


def run_a_simulation(bearer_token_input):
    headers = {
        'x-tenant-id': creds['tenant_ids'][ciam_creds],
        'Authorization': bearer_token_input,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", config_paths['MSM_DEV_BASE_URL'] + 'submit', headers=headers,
                                data=config_paths['sample_payload'])

    print(response.text)
    print("simulation running..")

    return response.json().get('data').get('run_ids')[0]


def get_kpi_results(bearer_token_input, scenario_id):
    time.sleep(20)

    url = f'{config_paths["MSM_DEV_BASE_URL"]}summary/{scenario_id}/kpi'
    payload = {}
    headers = {
        'x-tenant-id': creds['tenant_ids'][ciam_creds],
        'Authorization': bearer_token_input
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    fil = open("output_json/sample_kpi_single.json", "w")
    fil.write(response.text)
    fil.close()


if __name__ == '__main__':
    bearer_token = 'Bearer ' + get_CIAM_token()
    # scenario_id = run_a_simulation(bearer_token)
    # print(scenario_id)
    scenario_id = '60db895d3eb3ec5d7b0d78ad'
    get_kpi_results(bearer_token, scenario_id)
