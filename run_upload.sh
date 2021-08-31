#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Copy "collection" JSON files to Google Cloud Storage
gsutil cp output_json/collection/*.json gs://spa_sensitivity_analysis/raw_json

# Copy "collection" CSV files to Google Cloud Storage
gsutil cp output_csv/*.csv gs://spa_sensitivity_analysis/raw_csv