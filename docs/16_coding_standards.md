# Coding Standards & Guidelines Document

**Project Title:** An Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production  
**Document Version:** 1.0.0  
**Status:** Approved / Draft  
**Target Language:** Python 3.10+  
**Formatters & Linters:** Black, Flake8, Mypy  
**Date:** September 2026  

---

## 1. Code Formatting & Style Compliance

To ensure code consistency across Developer 1 and Developer 2, all Python code in `src/` and `tests/` MUST strictly comply with **PEP 8** style guidelines and pass automated CI checks.

### 1.1 Automated Tools Configuration
- **Formatter:** **Black** (Line length = 88 characters).
- **Linter:** **Flake8** (`--max-line-length=88 --ignore=E203,W503`).
- **Static Type Checker:** **Mypy** (`--strict` mode enabled for `src/`).

---

## 2. Naming Conventions Matrix

| Code Element | Style Schema | Example Pattern | Anti-Example (Forbidden) |
| :--- | :--- | :--- | :--- |
| **Modules / Files** | `snake_case.py` | `relational_joiner.py` | `RelationalJoiner.py`, `relational-joiner.py` |
| **Packages / Folders** | `snake_case` | `drift_engine` | `DriftEngine`, `drift-engine` |
| **Classes** | `PascalCase` | `PSICalculator`, `BatchRun` | `psi_calculator`, `PSI_Calculator` |
| **Functions / Methods** | `snake_case()` | `calculate_psi()` | `CalculatePSI()`, `calculatePsi()` |
| **Variables / Arguments** | `snake_case` | `batch_id`, `record_count` | `batchID`, `RecordCount` |
| **Global Constants** | `UPPER_SNAKE_CASE` | `PSI_CRITICAL_THRESHOLD = 0.25` | `psi_critical_threshold` |
| **Pydantic Schemas** | `PascalCase` | `FeatureDriftResponse` | `feature_drift_response` |
| **Database Tables** | `snake_case` (plural) | `batch_runs`, `alert_logs` | `BatchRun`, `batchRun` |

---

## 3. Type Annotations & Static Typing (Mypy)

Every function signature and class method MUST include explicit Python type hints for input parameters and return types.

### 3.1 Correct Example
```python
import pandas as pd
from typing import Dict, List, Optional

def compute_feature_drift(
    baseline_df: pd.DataFrame,
    target_df: pd.DataFrame,
    numerical_cols: List[str],
    threshold: float = 0.25
) -> Dict[str, float]:
    """Computes PSI scores for numerical columns."""
    results: Dict[str, float] = {}
    for col in numerical_cols:
        # calculation logic
        results[col] = 0.12
    return results
```

### 3.2 Incorrect Example (Strictly Prohibited)
```python
# FORBIDDEN: Missing type hints and ambiguous types
def compute_feature_drift(baseline, target, cols, threshold=0.25):
    results = {}
    # calculation logic
    return results
```

---

## 4. Documentation & Docstring Standards

All modules, classes, and public functions MUST include **Google-Style Python Docstrings**.

### 4.1 Function Docstring Format
```python
def calculate_psi(baseline_series: pd.Series, target_series: pd.Series, num_bins: int = 10) -> float:
    """Calculates the Population Stability Index (PSI) between baseline and target feature distributions.

    Args:
        baseline_series (pd.Series): Reference feature distribution from offline training.
        target_series (pd.Series): Production batch feature distribution to evaluate.
        num_bins (int, optional): Number of quantile bins to construct. Defaults to 10.

    Returns:
        float: Calculated PSI score.

    Raises:
        ValueError: If baseline_series or target_series contains zero valid records.
    """
    pass
```

---

## 5. Error Handling & Logging Standards

### 5.1 Exception Handling Principles
1. **Never Swallowing Exceptions:** Bare `except:` clauses are strictly forbidden. Catch specific exceptions (`KeyError`, `ValueError`, `SQLAlchemyError`).
2. **Explicit Custom Exceptions:** Domain-specific errors must inherit from custom base classes defined in `src/utils/exceptions.py`.
3. **Database Rollbacks:** All raw database operations MUST be wrapped in `try...except...finally` blocks with explicit session rollbacks on failure.

```python
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.utils.logger import logger

def save_batch_run(db: Session, batch_obj: models.BatchRun) -> models.BatchRun:
    try:
        db.add(batch_obj)
        db.commit()
        db.refresh(batch_obj)
        logger.info(f"Successfully persisted batch_id: {batch_obj.batch_id}")
        return batch_obj
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error(f"Database error during batch run persistence: {str(exc)}")
        raise RuntimeError("Failed to persist batch monitoring record.") from exc
```

### 5.2 Logging Standard
Use the centralized logger from `src/utils/logger.py` rather than print statements (`print()`).

```python
# FORBIDDEN
print("Processing started")

# CORRECT
from src.utils.logger import logger

logger.info("Initiating batch monitoring pipeline run.")
logger.warning("Feature 'mrr' showed moderate PSI drift (0.18).")
logger.error("Relational join failed: missing foreign key 'account_id'.")
```

---

## 6. Unit & Integration Testing Standards

### 6.1 Test Structure (AAA Pattern)
All unit tests in `tests/` MUST follow the **Arrange-Act-Assert** pattern:

```python
import pytest
import pandas as pd
from src.drift_engine.psi_calculator import PSICalculator

def test_psi_calculator_identical_distributions():
    # Arrange
    calculator = PSICalculator(num_bins=5)
    data = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0] * 20)
    
    # Act
    psi_score = calculator.calculate_psi(data, data)
    
    # Assert
    assert psi_score == pytest.approx(0.0, abs=1e-3)
```

---

## 7. Anti-Patterns & Code Smells to Avoid

1. **Hardcoded File Paths:** Never use absolute local file paths (e.g., `C:/Users/...`). Use `pathlib.Path` relative to project root.
2. **Global Mutable State:** Do not modify global variables inside functions. Pass parameters explicitly.
3. **Shadowing Standard Libraries:** Never name a module standard library names (e.g., naming a file `logging.py` or `random.py`).
4. **Direct DB Queries in Dashboard UI:** Streamlit UI code must NEVER import SQLAlchemy models or execute direct database queries; all communication must go through FastAPI REST endpoints.

---

## 8. Document Approval & Sign-Off

- **Prepared By:** Senior Technical Lead & Software Architect  
- **Reviewed By:** Developer 1 (Data Science) & Developer 2 (Backend)  
- **Status:** Approved as Engineering Coding Standard  

---
