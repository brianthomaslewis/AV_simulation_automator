import json

import yaml
from src.get_ciam_token import get_CIAM_token
# from src.get_sim_results import get_simulation_results
from src.kpi_to_csv import kpi_to_csv
from src.get_kpi_results import get_kpi_results, get_scenario_map
from src.merge_json import merge_json_files

# Set credentials (e.g. "msm_dev", "spa_dev", "spa_stage", "spa_prod") and output base path
ciam_creds = 'spa_dev'

if __name__ == '__main__':

    # Import YAML files
    with open('config/credentials.yaml') as cred_file:
        creds = yaml.load(cred_file, Loader=yaml.FullLoader)
    with open('config/params_paths.yaml') as path_file:
        config_paths = yaml.load(path_file, Loader=yaml.FullLoader)
    with open('input_data/params_scenario.yaml') as param_file:
        parameters = yaml.load(param_file, Loader=yaml.FullLoader)

    # Set kpi output base file path
    output_base_path = config_paths['kpi_base_path']

    # Obtain bearer_token
    bearer_token = 'Bearer ' + get_CIAM_token(client_id=creds['client_ids'][ciam_creds],
                                              client_secret=creds['client_secrets'][ciam_creds],
                                              ciam_url=config_paths["CIAM_URL"],
                                              proxy_dict=config_paths['proxy_dict'])

    # Obtain scenario map
    scenario_map = get_scenario_map(output_hash_fp=config_paths['hash_file_path'])

    # Retrieve multiple KPI/simulation results
    json_list = []
    for hash_id, scenario_id in scenario_map.items():
        content = get_kpi_results(bearer_token_input=bearer_token,
                                  api_base_url=config_paths['MSM_DEV_BASE_URL'],
                                  tenant_id=creds['tenant_ids'][ciam_creds],
                                  scenario_id=scenario_id,
                                  output_json_fp=f'{output_base_path}{hash_id}.json')

        # if content doesn't exist (job failed), skip; otherwise,append
        if content == 0:
            pass
        else:
            json_list.append(f'{output_base_path}{hash_id}.json')

    # Obtain title for collection
    title = parameters['title'][0]

    # Merge .json files
    merge_json_files(json_list, f'output_json/collection/{title}.json')

    # Convert .json collection to CSV
    kpi_to_csv(f'output_json/collection/{title}.json', f'output_csv/{title}.csv')
