"""
=========================================================
Module: clean_data.py

Purpose:
--------
Cleans the feature engineered dataset.

Tasks:
1. Remove unnecessary columns
2. Rename duplicate columns
3. Handle missing values
4. Convert boolean columns
5. Return clean dataset

Author: Sonal
=========================================================
"""

import pandas as pd


def clean_dataset(df):

    df = df.copy()

    # --------------------------------------------
    # Remove unnecessary columns
    # --------------------------------------------

    columns_to_drop = [
        "account_id",
        "account_name",
        "subscription_id",
        "signup_date",
        "plan_tier_x",
        "seats_x",
    ]

    df.drop(
        columns=columns_to_drop,
        inplace=True,
        errors="ignore"
    )

    # --------------------------------------------
    # Rename duplicate columns
    # --------------------------------------------

    df.rename(
        columns={
            "plan_tier_y": "plan_tier",
            "seats_y": "seats"
        },
        inplace=True
    )

    # --------------------------------------------
    # Convert Boolean Columns
    # --------------------------------------------

    boolean_columns = [
        "is_trial",
        "auto_renew_flag",
        "churn_flag"
    ]

    for col in boolean_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.upper()
                .map({
                    "TRUE": 1,
                    "FALSE": 0
                })
            )

    # --------------------------------------------
    # Fill Numerical Missing Values
    # --------------------------------------------

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numerical_columns:

        df[col] = df[col].fillna(
            df[col].median()
        )

    # --------------------------------------------
    # Fill Categorical Missing Values
    # --------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_columns:

        df[col] = df[col].fillna("Unknown")

    return df