# Load modules
import json
import time
from datetime import datetime
from itertools import product
import yaml
from src.get_ciam_token import get_CIAM_token
from src.get_baseline_simulation_request import create_key, create_payload_combination
from src.post_simulation_request import post_simulation_request

# Set credentials (e.g. "msm_dev", "spa_dev", "spa_stage", "spa_prod")
ciam_creds = 'spa_dev'


def execute_simulations(input_scenario_json_fp, bearer_token_input, params_dict,
                        tenant_id, api_base_url, output_hash_fp):
    scenario_lookup_hash = {}

    parallel_threshold_counter = 1
    for param_iteration in product(*params_dict.values()):
        iter_dict = dict(zip(params_dict.keys(), param_iteration))
        # TODO: Add logic for time-windows
        lookup_key = create_key(date=datetime.now().strftime("%Y-%m-%d"),
                                title=iter_dict['title'],
                                num_vehicles=iter_dict['num_vehicles'],
                                load_time=iter_dict['load_times'],
                                unload_time=iter_dict['unload_times']
                                )

        payload = create_payload_combination(input_scenario_json_fp, **iter_dict)
        scenario_lookup_hash[lookup_key] = post_simulation_request(bearer_token_input, payload,
                                                                   tenant_id=tenant_id,
                                                                   api_base_url=api_base_url)
        # Don't run too many sims at once or we'll have problems - MSM infrastructure limitation
        if parallel_threshold_counter % 5 == 0:
            print(
                f"{int(parallel_threshold_counter / 5)}th batch of 5 sims submitted.\n"
                f"Allowing space to free. Please wait..")
            time.sleep(240)
            print(".. space free.")
        parallel_threshold_counter += 1

    with open(output_hash_fp, 'w') as outfile:
        json.dump(scenario_lookup_hash, outfile, indent=0)


if __name__ == '__main__':
    # Import YAML files
    with open('config/credentials.yaml') as cred_file:
        creds = yaml.load(cred_file, Loader=yaml.FullLoader)
    with open('config/params_paths.yaml') as path_file:
        config_paths = yaml.load(path_file, Loader=yaml.FullLoader)
    with open('input_data/params_scenario.yaml') as param_file:
        parameters = yaml.load(param_file, Loader=yaml.FullLoader)

    # Obtain bearer_token
    bearer_token = 'Bearer ' + get_CIAM_token(client_id=creds['client_ids'][ciam_creds],
                                              client_secret=creds['client_secrets'][ciam_creds],
                                              ciam_url=config_paths["CIAM_URL"],
                                              proxy_dict=config_paths['proxy_dict'])

    # Execute simulations
    execute_simulations(input_scenario_json_fp=config_paths['input_scenario_json'],
                        bearer_token_input=bearer_token,
                        params_dict=parameters,
                        tenant_id=creds['tenant_ids'][ciam_creds],
                        api_base_url=config_paths['MSM_DEV_BASE_URL'],
                        output_hash_fp=config_paths['hash_file_path']
                        )
