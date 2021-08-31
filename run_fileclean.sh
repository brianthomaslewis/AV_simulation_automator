#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Remove old files and create new directories if they don't exist
rm hash_data/*.json
rm output_json/individual/*.json
rm output_json/collection/*.json
rm output_csv/*.csv
mkdir -p hash_data

mkdir -p output_json/individual
mkdir -p output_json/collection
mkdir -p output_csv