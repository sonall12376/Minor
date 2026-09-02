"""
======================================================
Module Name : load_data.py

Purpose:
Reads all raw CSV files from data/raw/

Input:
accounts.csv
subscriptions.csv
feature_usage.csv
support_tickets.csv
churn_events.csv

Output:
accounts_df
subscriptions_df
feature_usage_df
support_tickets_df
churn_events_df

This module ONLY loads data.
No cleaning.
No merging.
No preprocessing.
======================================================
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"

def load_data():
    accounts_df=pd.read_csv(RAW_DATA/"accounts.csv")
    subscriptions_df=pd.read_csv(RAW_DATA/"subscriptions.csv")
    feature_usage_df=pd.read_csv(RAW_DATA/"feature_usage.csv")
    support_tickets_df=pd.read_csv(RAW_DATA/"support_tickets.csv")
    churn_events_df=pd.read_csv(RAW_DATA/"churn_events.csv")

    return{
        "accounts":accounts_df,
        "subscriptions":subscriptions_df,
        "feature_usage":feature_usage_df,
        "support_tickets":support_tickets_df,
        "churn_events":churn_events_df,
    }

# if __name__ == "__main__":
#     data = load_data()

#     for name, df in data.items():
#         print(f"{name}: {df.shape}")
