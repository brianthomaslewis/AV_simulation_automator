import glob
import os

import pandas as pd


def merge_csv(input_folder, output_path):
    path = input_folder
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv(output_path, index=False)
