"""
=========================================================
Module : preprocess_pipeline.py

Purpose
--------
Runs the complete preprocessing pipeline.

Pipeline

Load Data
↓

Merge Tables
↓

Feature Engineering
↓

Clean Data
↓

Encode Features
↓

Save Final Dataset

Author:
Sonal
=========================================================
"""

from pathlib import Path

from load_data import load_data
from merge_tables import (
    create_subscription_summary,
    create_usage_summary,
    create_support_summary,
    merge_all_tables,
)

from feature_engineering import create_features

from clean_data import clean_dataset

from encode_features import encode_dataset

import pandas as pd

def run_preprocessing_pipeline():
        # ==========================================
    # Load Raw Data
    # ==========================================

    data = load_data()

    accounts_df = data["accounts"]

    subscriptions_df = data["subscriptions"]

    feature_usage_df = data["feature_usage"]

    support_df = data["support_tickets"]

        # ==========================================
    # Create Summary Tables
    # ==========================================

    subscription_summary = create_subscription_summary(
        subscriptions_df
    )

    usage_summary = create_usage_summary(
        feature_usage_df
    )

    support_summary = create_support_summary(
        support_df
    )

        # ==========================================
    # Merge Tables
    # ==========================================

    merged_dataset = merge_all_tables(
        accounts_df,
        subscription_summary,
        usage_summary,
        support_summary,
    )

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    INTERIM_PATH = PROJECT_ROOT / "data" / "interim"

    merged_dataset.to_csv(
        INTERIM_PATH / "merged_dataset.csv",
        index=False
    )

        # ==========================================
    # Feature Engineering
    # ==========================================

    featured_dataset = create_features(
        merged_dataset
    )

    featured_dataset.to_csv(
        INTERIM_PATH / "feature_engineered_dataset.csv",
        index=False
    )

        # ==========================================
    # Cleaning
    # ==========================================

    cleaned_dataset = clean_dataset(
        featured_dataset
    )

    cleaned_dataset.to_csv(
        INTERIM_PATH / "cleaned_dataset.csv",
        index=False
    )

        # ==========================================
    # Encoding
    # ==========================================

    encoded_dataset, encoders = encode_dataset(
        cleaned_dataset
    )

    encoded_dataset.to_csv(
        INTERIM_PATH / "encoded_dataset.csv",
        index=False
    )

    PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

    encoded_dataset.to_csv(
        PROCESSED_PATH / "final_dataset.csv",
        index=False
    )

    return encoded_dataset

if __name__ == "__main__":

    final_dataset = run_preprocessing_pipeline()

    print()

    print("Preprocessing Pipeline Completed Successfully!")

    print()

    print(final_dataset.head())

    print()

    print(final_dataset.shape)


    
    
    