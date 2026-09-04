"""
=========================================================
Module: feature_engineering.py

Purpose:
--------
Creates new machine learning features from the merged dataset.

Input:
------
final_dataset_df

Output:
-------
feature_engineered_df

Author:
Sonal
=========================================================
"""

import pandas as pd


def create_features(final_dataset):

    df = final_dataset.copy()

    # ---------------------------------------------------
    # Convert signup_date to datetime
    # ---------------------------------------------------

    df["signup_date"] = pd.to_datetime(df["signup_date"])

    # ---------------------------------------------------
    # Account Age
    # ---------------------------------------------------

    df["account_age_days"] = (
        pd.Timestamp.today() - df["signup_date"]
    ).dt.days

    # ---------------------------------------------------
    # Revenue Per Seat
    # ---------------------------------------------------

    df["revenue_per_seat"] = (
        df["mrr_amount"] /
        df["seats_y"].replace(0, 1)
    )

    # ---------------------------------------------------
    # Customer Activity Score
    # ---------------------------------------------------

    df["customer_activity_score"] = (
        df["total_usage"]
        - (df["total_support_tickets"] * 5)
        - (df["total_errors"] * 2)
    )

    # ---------------------------------------------------
    # Ticket Resolution Efficiency
    # ---------------------------------------------------

    df["ticket_resolution_efficiency"] = (
        1 /
        (df["average_resolution_time"] + 1)
    )

    # ---------------------------------------------------
    # Usage Per Feature
    # ---------------------------------------------------

    df["usage_per_feature"] = (
        df["total_usage"] /
        df["unique_features_used"].replace(0, 1)
    )

    # ---------------------------------------------------
    # Error Rate
    # ---------------------------------------------------

    df["error_rate"] = (
        df["total_errors"] /
        df["total_usage"].replace(0, 1)
    )

    # ---------------------------------------------------
    # Satisfaction Index
    # ---------------------------------------------------

    df["satisfaction_index"] = (
        df["average_satisfaction"] *
        df["ticket_resolution_efficiency"]
    )

    return df