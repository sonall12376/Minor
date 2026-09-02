import pandas as pd


def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)


def preprocess_data(df):
    """Basic preprocessing pipeline."""
    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing numerical values
    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].median())

    return df


if __name__ == "__main__":
    print("Preprocessing module loaded successfully.")