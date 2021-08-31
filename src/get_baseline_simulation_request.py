import json
from datetime import datetime


# Function to create key identifying particular iteration
def create_key(title, load_time, unload_time, num_vehicles, date):
    return f'{date}_{title}_veh_{num_vehicles}_lt_{load_time}_ut_{unload_time}'


# Function to create payload combination iterating through multiple parameter toggles
def create_payload_combination(input_scenario_json_fp,
                               title, solver_name, solver_id, map_provider,
                               load_times, unload_times,
                               vehicle_capacity, num_vehicles, fleet_type):
    with open(input_scenario_json_fp) as f:
        payload = json.load(f)

    # scenarioDescription parameters
    payload["scenario"]["scenarioDescription"]["title"] = title
    payload["scenario"]["scenarioDescription"]["solverId"] = solver_id
    payload["scenario"]["scenarioDescription"]["solver"] = solver_name
    payload["scenario"]["scenarioDescription"]["mappingProvider"] = map_provider

    # riderParameters parameters
    payload["scenario"]["riderParameters"][0]["loadTime"] = load_times
    payload["scenario"]["riderParameters"][0]["unloadTime"] = unload_times

    # vehicleParameters
    payload["scenario"]["vehicleParameters"]["capacity"] = vehicle_capacity
    payload["scenario"]["vehicleParameters"]["numberOfVehicles"] = num_vehicles
    payload["scenario"]["vehicleParameters"]["numberOfVehiclesStart"] = num_vehicles
    payload["scenario"]["vehicleParameters"]["numberOfVehiclesStep"] = 0
    payload["scenario"]["vehicleParameters"]["numberOfVehiclesStop"] = num_vehicles
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["count"] = num_vehicles
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["type"] = fleet_type
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["configuration"] = [{f"{fleet_type}": 1}]

    # date parameter (datetime)
    payload["scenario"]["date"] = datetime.now().strftime("%b %d, %y %I:%M:%S %p")

    return payload


def check_payload(input_scenario_json_fp):
    with open(input_scenario_json_fp) as f:
        payload = json.load(f)

    # vehicleParameters
    payload["scenario"]["vehicleParameters"]["numberOfVehicles"] = 10
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["count"] = 10
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["type"] = 'BILLY_BOB'
    payload["scenario"]["vehicleParameters"]["fleetConfiguration"][0]["configuration"] = [{"BILLY_BOB": 1}]

    return payload


# if __name__ == '__main__':
#     data = check_payload('../input_data/input_scenario.json')
#     with open('../output_json/PAYLOAD2.json', 'w') as f:
#         json.dump(data, f, indent=4)
#     print(data)

# def is_list_non_negative(list_item):
#     for value in list_item:
#         if value <= 0:
#             return False
#     return True
#
#
# def is_valid_parameters(data):
#     for key in data.keys():
#         if type(data[key]) == list:
#             if not is_list_non_negative(data[key]):
#                 return False
#     return True
