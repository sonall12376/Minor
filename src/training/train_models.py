"""
=========================================================
Module : train_models.py

Purpose
--------
Loads the final dataset and trains
multiple machine learning models.

Models:
1. Logistic Regression
2. Decision Tree
3. Random Forest

This module DOES NOT:
- Evaluate models
- Save models
- Select best model

Author:
Sonal
=========================================================
"""

from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from evaluate_models import evaluate_models


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "final_dataset.csv"
)


def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    return df




def split_dataset(df):

    X = df.drop(columns=["churn_flag"])

    y = df["churn_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


def train_models(X_train, y_train):

    logistic_model = LogisticRegression(
        random_state=42,
        max_iter=5000,
        class_weight="balanced"
    )

    decision_tree_model = DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced"
    )

    random_forest_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    logistic_model.fit(X_train, y_train)

    decision_tree_model.fit(X_train, y_train)

    random_forest_model.fit(X_train, y_train)

    return {
        "Logistic Regression": logistic_model,
        "Decision Tree": decision_tree_model,
        "Random Forest": random_forest_model,
    }


if __name__ == "__main__":

    dataset = load_dataset()

    print(dataset["churn_flag"].value_counts())
    print()
    print(dataset["churn_flag"].value_counts(normalize=True))

    print("\n==============================")
    print("AVERAGE VALUES BY CHURN CLASS")
    print("==============================")
    print(dataset.groupby("churn_flag").mean())
    print("\n==============================")
    print("CORRELATION WITH CHURN")
    print("==============================")
    print(dataset.corr(numeric_only=True)["churn_flag"].sort_values())

    X_train, X_test, y_train, y_test = split_dataset(dataset)


    print("\nTraining Distribution")
    print(y_train.value_counts())

    print("\nTesting Distribution")
    print(y_test.value_counts())

    models = train_models(
        X_train,
        y_train
    )

    results = evaluate_models(
    models,
    X_test,
    y_test
)
    rf_predictions = models["Random Forest"].predict(X_test)
    print("\nRandom Forest Predictions")
    print(pd.Series(rf_predictions).value_counts())

    print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

for model_name, metrics in results.items():

    print(f"\nModel : {model_name}")

    print(f"Accuracy  : {metrics['accuracy']:.4f}")

    print(f"Precision : {metrics['precision']:.4f}")

    print(f"Recall    : {metrics['recall']:.4f}")

    print(f"F1 Score  : {metrics['f1_score']:.4f}")

print(dataset.isnull().sum())

print(dataset.dtypes)

print(dataset.describe())