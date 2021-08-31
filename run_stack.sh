#!/bin/bash
export IND_FILE_PATTERN='gs://spa_sensitivity_analysis/raw_csv/miami_req_100_term_2_*.csv'
export IND_DIRECTORY='gs://spa_sensitivity_analysis/raw_csv/miami_req_100_term_2_transloc/*.csv'
export COMBINED_SUFFIX='miami_req_100_term_2.csv'

# Activate virtual environment
source venv/Scripts/activate

# Move individual files to correct folder
gsutil mv $IND_FILE_PATTERN $IND_DIRECTORY

# Copy down individual files and then combine them
gsutil -m cp $IND_DIRECTORY to_combine/
python -c 'from src.merge_csv import merge_csv; merge_csv("to_combine/", "combined/combined.csv")'
mv combined/combined.csv "combined/${COMBINED_SUFFIX}"

# Upload combined file to GCS
gsutil cp "combined/${COMBINED_SUFFIX}" "gs://spa_sensitivity_analysis/combined/${COMBINED_SUFFIX}"