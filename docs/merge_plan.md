| Step                           | Python File              | Input                             | Output                             |
| ------------------------------ | ------------------------ | --------------------------------- | ---------------------------------- |
| Load Data                      | `load_data.py`           | 5 CSV files                       | 5 DataFrames                       |
| Merge Accounts + Subscriptions | `merge_tables.py`        | `accounts_df`, `subscriptions_df` | `account_subscription_df`          |
| Aggregate Feature Usage        | `feature_engineering.py` | `feature_usage_df`                | `usage_summary_df`                 |
| Aggregate Support Tickets      | `feature_engineering.py` | `support_tickets_df`              | `support_summary_df`               |
| Final Merge                    | `merge_tables.py`        | All intermediate DataFrames       | `final_dataset_df`                 |
| Save Dataset                   | `preprocess_pipeline.py` | `final_dataset_df`                | `data/processed/final_dataset.csv` |
