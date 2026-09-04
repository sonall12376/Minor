"""
=========================================================
Module: encode_features.py

Purpose:
--------
Encodes categorical columns into numerical values.

Author: Sonal
=========================================================
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def encode_dataset(df):

    df = df.copy()

    label_encoders = {}

    categorical_columns = [
        "industry",
        "country",
        "referral_source",
        "plan_tier",
        "billing_frequency"
    ]

    for col in categorical_columns:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

        label_encoders[col] = encoder

    return df, label_encoders