# The MSM SPAutomator&trade;

## Project Flowchart:
![Flowchart](https://github.com/brianthomaslewis/AV_simulation_automator/blob/main/img/flowchart.png)


## Introduction:

This codebase is designed to accomplish two goals:

   1. For a single **demand AND depot scenario**, batch-automate MSM API calls across combinations of the following parameters:
      - Solver
      - Load Time
      - Unload Time
      - \# of Vehicles Available
      

   2. Store the results in GCP:
      - Raw data `->` Cloud Storage bucket `gs://spa_sensitivity_analysis/raw_json`
      - Formatted data `->` Cloud Storage bucket `gs://spa_sensitivity_analysis/raw_csv`

## Step 1: Download and install Google Cloud SDK (if needed) 
In order to interact with GCP following the API calls, you will need to [download and install Google Cloud's SDK](https://cloud.google.com/sdk/docs/install) if you have not already done so.
This will be used to interact with your `@avmobility.io` GCP account.

## Step 2: Create a virtual environment (`venv`) and install requirements.txt

From the root of the repository, run the following command:

```bash
python -m venv ./venv
source venv/Scripts/activate # for Windows users
pip install -r requirements.txt
```

## Step 3: Specify `config/credentials.yaml`

### What is `credentials.yaml`?
It is a YAML file that provides the credentials necessary to interact with MSM. The format is as follows: 

```
# Credentials
tenant_ids:
  spa_dev: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  spa_stage: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  spa_prod: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  msm_dev: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

client_ids:
  spa_dev: 'xxxxxxxxxxxxxxxxxxxx'
  spa_stage: 'xxxxxxxxxxxxxxxxxxxx'
  spa_prod: 'xxxxxxxxxxxxxxxxxxxx'
  msm_dev: 'xxxxxxxxxxxxxxxxxxxx'

client_secrets:
  spa_dev: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  spa_stage: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  spa_prod: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  msm_dev: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Solvers
solvers:
  mozart_online_id: 'xxxxxxxxxxxxxxxxxxxx'
  mozart_online_name: 'Mozart GA Online'

  mozart_sched_id: 'xxxxxxxxxxxxxxxxxxxx'
  mozart_sched_name: 'Mozart GA Scheduler'

  charity_id: 'xxxxxxxxxxxxxxxxxxxx'
  charity_name: 'MSM Charity Pilot'

  transloc_id: 'xxxxxxxxxxxxxxxxxxxx'
  transloc_name: 'TransLoc Ride Hail'

  hub_id: 'xxxxxxxxxxxxxxxxxxxx'
  hub_name: 'Hub Delivery'

  campus_id: 'xxxxxxxxxxxxxxxxxxxx'
  campus_name: 'Campus Safe Ride Hail'
```

### How do I obtain `credentials.yaml`?
This file is not saved to the repository as it contains sensitive credential information. 
These credentials can be obtained by contacting the MSM product team. 

## Step 4: Specify `input_data/input_scenario.json`

### What is `input_scenario.json`?

It is a JSON file that provides the baseline structure for a single **demand AND depot scenario** to call the API. 


Put another way, the input parameters listed in the [introduction](#introduction) are toggled across multiple values, 
but remaining elements of the API call stay fixed to the structure provided in this file.

### How do I obtain `input_scenario.json`?
(This assumes some prior familiarity with the GUI version of the Mobility Service Modeler, or MSM.)

1. Open the MSM GUI within the `dev` environment here: https://dev-hyper-driver.apps.pp01i.edc1.cf.ford.com/home.
2. Click the ` + New` button to create a baseline scenario with the desired demand (requests) file.
3. Once that simulation has finished running, return to the main MSM landing page.
4. Find the `Intermediate Files` link, and download those files by clicking on the icon (see example below).

![MSM_1](https://github.com/brianthomaslewis/AV_simulation_automator/blob/main/img/msm_1.png)

5. Open the downloaded `.zip` file and locate the `submission_xxx.json` file (see example below).

![MSM_2](https://github.com/brianthomaslewis/AV_simulation_automator/blob/main/img/msm_2.png)

6. Copy this file and save it to `input_data/input_scenario.json`.

## Step 5: Specify `input_data/params_scenario.yaml`

### What is `params_scenario.yaml`?
It is a YAML file that provides the set and values of parameters which will be toggled within 
the single **demand AND depot scenario** specified in [Step 1](#step-1-specify-input_datainput_scenariojson).

### How do I make changes to `params_scenario.yaml`?
It can be edited directly using any text editor or Python IDE.

The format is as follows:

```
### scenarioDescription parameters ###
title: ["miami_req_100"]
solver_name: ["Transloc Ride Hail"]
solver_id: ["xxxxxxxxxxxxxxxx"]
map_provider: ["HERE_MAPS"]

### fleetDemand parameters ###
load_times: [1, 3, 5]
unload_times: [2, 4]
fleet_occupancy: [1]

### vehicleParameters ###
vehicle_capacity: ["1"]
num_vehicles: [5, 10, 15, 20]
fleet_type: ["AMBULATORY"]
```

The most common fields to toggle are:
- `solver_name` and `solver_id` (they must be correctly paired to avoid errors)
- `load_times`
- `unload_times`
- `num_vehicles`

The SPAutomator&trade; will create a grid of all possible combinations of parameters included, but you may run into errors or simulation failures 
if the total number of combinations > ~25. 

In the example given above, `load_times` has 3 distinct values, `unload_times` has 2 distinct values, and `num_vehicles` has 4 distinct values. 
All other parameters have 1 distinct value. So this will result in a grid of [3 * 2 * 4 =] 24 combinations.

## Step 6: Run the SPAutomator&trade;

1. Specify `input_data/input_scenario.json` and `input_data/parameters.yaml` appropriately.
2. Place correct `config/credentials.yaml` file into the repository for YAML sourcing.
3. Connect to the Ford VPN.
4. Open Linux/Unix (or GitBash) terminal and run the following from the root of the repository:
```bash
gcloud auth login
```

This command will open up a tab in your internet browser and  require that you log in to Google Cloud.
This will authorize your `gsutil` SDK profile and allow you to interact with GCP without throwing credential errors.

5. Run the following commands in your terminal:
```bash
bash run_fileclean.sh  # Cleans out file directories if they have old data
bash run_sims.sh # Kicks off simulation runs
```

This will clean out any lingering files or data in the appropriate folders and kick off the batches of simulations with
the parameters specified in `parameters.yaml`. You can monitor the progress of these simulations in real-time at https://dev-hyper-driver.apps.pp01i.edc1.cf.ford.com/home. 
**Wait until all of the simulations have finished running before proceeding.** 

6. Run the following command in your terminal:

```bash
bash run_fetch.sh # Fetches simulation runs once completed (skips "FAILED" runs)
```

This will collect, process, and upload your batch of simulations to GCP.

7. [OPTIONAL, MAY BE NEEDED] Run the following command in your terminal after disconnecting from the VPN:

```bash
bash run_upload.sh # Uploads separately with VPC restrictions
bash run_stack.sh # Stacks multi-batch runs into one CSV
```

This will stack multiple simulation runs across a "demand AND depot scenario" into one CSV. 
**The `run_stack.sh` file should be modified accordingly to match file path patterns in order to work as intended.** 


——————————————————————————————————

### Goal details:

1. **Running simulations**:
   - Reads in input, modeled off of a baseline sim using a previously existing script
   - Authenticates through CIAM
   - Iterates through combinations by reading in parameter data
   - Runs simulation combinations in batches of 5 until all are finished (this is due to MSM DEV infrastructure limit)
     - Populates a hash map while running sims


2. **Retrieving simulations**:
   - Authenticates through CIAM
   - Retrieves simulations by reading based on `scenario_id` values found in the hash map and calling MSM API
   - Populates individual JSON files, and then is appended into a "collection" of JSON files
   - These are cleaned into a "collection"-level CSV file 
   - Using `gsutil`, scenario "collections" in JSON and CSV are copied to Google Cloud Storage buckets  


3. **Using a "Data Transfer" scheduled job in GCP**
   - CSV files (with consistent format) are copied over into a BigQuery table


4. **Build out Data Studio dashboard using data pulled in from BigQuery table**
   - There will be a separate tab for each scenario "collection"















