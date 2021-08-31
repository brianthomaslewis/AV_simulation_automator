#!/bin/bash

# Activate virtual environment
source venv/Scripts/activate

# Retrieve simulations and merge individual files into a "collection"
python run_retrieval.py