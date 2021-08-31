import json
import warnings
from datetime import datetime
import pandas as pd

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def kpi_to_csv(json_fp, output_fp):
    # Import JSON file taken from simulation output kpi file
    fil = open(json_fp)
    json_file = json.load(fil)

    # Iterate through each scenario run included in "collection" JSON file
    run_list = []
    for run in json_file:

        fp_title = run['scenarioData']['title']

        # Convert kpi output to pandas df
        df_main = pd.json_normalize(run)

        # Drop columns that vary by API call
        # Currently, this will drop all request/customer-level, vehicle-level, timestamp-level, and
        # riderType-level fields
        df_main.drop(list(df_main.filter(
            regex=r'ByRequest|byRequest|byrequest|by_request|perVehicle|pervehicle|per_vehicle|ByCustomer'
                  r'|timeSeriesKpis|Binning|binning|byRiderType')),
            axis=1, inplace=True)

        # Clean up column names
        df_main.columns = df_main.columns.str.replace(".", "_").\
                                          str.replace("-", " ").\
                                          str.replace(" ", "_").\
                                          str.replace("_{2,}", "_")

        # Reorder columns
        title = df_main.pop('scenarioData_title')
        scenario_id = df_main.pop('scenarioData_runID')
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_main.insert(0, 'scenarioData_title', title)
        df_main.insert(0, 'scenario_id', scenario_id)
        df_main.insert(0, 'run_datetime', date)

        # Convert df_main back to dict
        run_dict = df_main.to_dict(orient='records')
        run_list.extend(run_dict)

    # Export dataframe to CSV
    output = pd.DataFrame(run_list)
    output.to_csv(output_fp, index=False)
