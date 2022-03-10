import pandas as pd
import numpy as np
import os
import glob

def load_full_df(CSV_DIR_STRING, JSON_DIR_STRING, TARGET_COL_NAME='label', load_json=True):
    
    all_files = glob.glob(CSV_DIR_STRING + "/*.csv")
    df = pd.concat((pd.read_csv(f) for f in all_files))

    if load_json:
        marketplace = pd.read_json(JSON_DIR_STRING + 'marketplace.json')
        category = pd.read_json(JSON_DIR_STRING + 'category.json')
        marketplace.rename(columns={'name': 'country_marketplace'}, inplace=True)
        category.rename(columns={'name': 'category_name'}, inplace=True)

        df = df.merge(marketplace, left_on='marketplace_id', right_on='id')
        df = df.merge(category, left_on='product_category_id', right_on='id')

        column_to_move = df.pop(TARGET_COL_NAME)

        df.insert(len(df.columns), TARGET_COL_NAME, column_to_move)

    return df

def delete_columns(df, columns_to_delete=[]):
    for i in range(len(columns_to_delete)):
        del df[columns_to_delete[i]]