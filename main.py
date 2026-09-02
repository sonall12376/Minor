"""
Main entry point for the Automated MLOps Model Monitoring Framework.
"""

from src.preprocessing.preprocess import preprocess_data


def main():
    print("=" * 60)
    print("Automated MLOps Model Monitoring Framework")
    print("=" * 60)

    print("\nPipeline:")
    print("1. Data Preprocessing")
    print("2. Baseline Model Training")
    print("3. Baseline Profiling")
    print("4. Production Data Monitoring")
    print("5. Drift Detection")
    print("6. SHAP-based Diagnosis")
    print("7. Performance Evaluation")
    print("8. Model Health Reporting")

    print("\nMLOps monitoring pipeline initialized.")


if __name__ == "__main__":
    main()