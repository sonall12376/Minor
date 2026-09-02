# Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production

## Project Overview

This project develops an automated MLOps framework for monitoring machine learning models after deployment.

The framework detects changes in production data, identifies potential model degradation, and provides feature-level diagnosis using SHAP values.

## Project Pipeline

```text
Dataset
   ↓
Data Preprocessing
   ↓
Baseline Model Training
   ↓
Baseline Profile
   ├── Feature Distributions
   ├── Model Performance
   └── SHAP Values
   ↓
Production Data
   ↓
Production Data Logging
   ↓
Statistical Drift Detection
   ↓
Significant Drift?
   ├── No → Healthy Model
   │
   └── Yes
        ↓
     SHAP Diagnosis
        ↓
   Feature-Level Diagnosis
        ↓
   Ground Truth Available?
        ├── Yes → Performance Evaluation
        └── No  → Degradation Unconfirmed
        ↓
   Model Health Report
        ↓
     Dashboard