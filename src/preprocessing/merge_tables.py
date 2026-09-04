"""
=========================================================
Module: merge_tables.py

Purpose:
Creates summary tables from the relational dataset and
merges them into one ML-ready dataset.

Author: Sonal
=========================================================
"""

import pandas as pd

from load_data import load_data
from pathlib import Path
from feature_engineering import create_features
from clean_data import clean_dataset
from encode_features import encode_dataset



# =========================================================
# Subscription Summary
# =========================================================

def create_subscription_summary(subscriptions_df):

    subscriptions_df = subscriptions_df.copy()

    subscriptions_df["start_date"] = pd.to_datetime(
        subscriptions_df["start_date"]
    )

    # Sort subscriptions so latest subscription comes last
    subscriptions_df = subscriptions_df.sort_values(
        ["account_id", "start_date"]
    )

    # Latest subscription for every account
    latest_subscription = (
        subscriptions_df
        .groupby("account_id")
        .last()
        .reset_index()
    )

    # Total upgrades
    upgrade_summary = (
        subscriptions_df
        .groupby("account_id")["upgrade_flag"]
        .sum()
        .reset_index()
        .rename(columns={"upgrade_flag": "total_upgrades"})
    )

    # Total downgrades
    downgrade_summary = (
        subscriptions_df
        .groupby("account_id")["downgrade_flag"]
        .sum()
        .reset_index()
        .rename(columns={"downgrade_flag": "total_downgrades"})
    )

    latest_subscription = latest_subscription.merge(
        upgrade_summary,
        on="account_id",
        how="left"
    )

    latest_subscription = latest_subscription.merge(
        downgrade_summary,
        on="account_id",
        how="left"
    )

    latest_subscription["subscription_age_days"] = (
        pd.Timestamp.today()
        - latest_subscription["start_date"]
    ).dt.days

    subscription_summary = latest_subscription[
        [
            "subscription_id",
            "account_id",
            "plan_tier",
            "seats",
            "mrr_amount",
            "arr_amount",
            "billing_frequency",
            "auto_renew_flag",
            "subscription_age_days",
            "total_upgrades",
            "total_downgrades",
        ]
    ]

    return subscription_summary


# =========================================================
# Feature Usage Summary
# =========================================================

def create_usage_summary(feature_usage_df):

    usage_summary = (
        feature_usage_df
        .groupby("subscription_id")
        .agg(
            total_usage=("usage_count", "sum"),
            average_usage=("usage_count", "mean"),
            average_usage_duration=("usage_duration_secs", "mean"),
            total_errors=("error_count", "sum"),
            beta_feature_usage=("is_beta_feature", "sum"),
            unique_features_used=("feature_name", "nunique")
        )
        .reset_index()
    )

    return usage_summary


# =========================================================
# Support Ticket Summary
# =========================================================

def create_support_summary(support_df):

    support_summary = (
        support_df
        .groupby("account_id")
        .agg(
            total_support_tickets=("ticket_id", "count"),
            average_resolution_time=("resolution_time_hours", "mean"),
            average_first_response_time=(
                "first_response_time_minutes",
                "mean"
            ),
            average_satisfaction=("satisfaction_score", "mean"),
            escalation_count=("escalation_flag", "sum")
        )
        .reset_index()
    )

    return support_summary

def merge_all_tables(
    accounts_df,
    subscription_summary_df,
    usage_summary_df,
    support_summary_df,
):

    # Merge subscription summary with usage summary
    subscription_usage_df = subscription_summary_df.merge(
        usage_summary_df,
        on="subscription_id",
        how="left"
    )

    # Merge everything with accounts
    final_dataset = accounts_df.merge(
        subscription_usage_df,
        on="account_id",
        how="left"
    )

    # Merge support summary
    final_dataset = final_dataset.merge(
        support_summary_df,
        on="account_id",
        how="left"
    )

    return final_dataset

