"""
=========================================================
Module : evaluate_models.py

Purpose
--------
Evaluates all trained machine learning models.

Metrics:
1. Accuracy
2. Precision
3. Recall
4. F1 Score

Author:
Sonal
=========================================================
"""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def evaluate_models(models, X_test, y_test):

    results = {}

    for model_name, model in models.items():

        predictions = model.predict(X_test)

        results[model_name] = {

            "accuracy": accuracy_score(y_test, predictions),

            "precision": precision_score(
                y_test,
                predictions,
                zero_division=0
            ),

            "recall": recall_score(
                y_test,
                predictions,
                zero_division=0
            ),

            "f1_score": f1_score(
                y_test,
                predictions,
                zero_division=0
            ),

            "confusion_matrix": confusion_matrix(
                y_test,
                predictions
            )
        }

    return results