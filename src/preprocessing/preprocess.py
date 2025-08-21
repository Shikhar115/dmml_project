import os
import logging
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

logging.basicConfig(filename="ingestion.log", level=logging.INFO)

def preprocess_csv():
    df = pd.read_csv("raw_data/" + sorted(os.listdir("./raw_data"))[-2])
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = df.select_dtypes(exclude=['float64', 'int64']).columns

    df[num_cols] = SimpleImputer(strategy='mean').fit_transform(df[num_cols])
    df[cat_cols] = SimpleImputer(strategy='most_frequent').fit_transform(df[cat_cols])
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    df[num_cols] = StandardScaler().fit_transform(df[num_cols])
    df.to_csv("clean_churn_csv.csv", index=False)

def preprocess_api():
    df = pd.read_csv("raw_data/" + sorted(os.listdir("./raw_data"))[-1])
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = df.select_dtypes(exclude=['float64', 'int64']).columns

    df[num_cols] = SimpleImputer(strategy='mean').fit_transform(df[num_cols])
    df[cat_cols] = SimpleImputer(strategy='most_frequent').fit_transform(df[cat_cols])
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    df[num_cols] = StandardScaler().fit_transform(df[num_cols])
    df.to_csv("clean_churn_api.csv", index=False)
