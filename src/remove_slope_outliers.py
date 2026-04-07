from pathlib import Path

import pandas as pd

from src.config import (
    FINAL_DATA_VISIT_TO_VISIT_FILE,
    FINAL_DATA_WITHOUT_SLOPE_OUTLIERS_FILE,
    MSSS_COLUMN,
    SLOPE_FEATURE_KEYWORD,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataset for outlier removal."""
    df = df.copy()
    df = df.dropna(subset=[MSSS_COLUMN]).copy()
    return df


def get_slope_features(df: pd.DataFrame, keyword: str = SLOPE_FEATURE_KEYWORD) -> list[str]:
    """Return all column names containing the slope keyword."""
    return [column for column in df.columns if keyword in column]


def get_non_outlier_mask(df: pd.DataFrame, column_name: str) -> pd.Series:
    """Return a boolean mask for rows within IQR bounds for one column."""
    q1 = df[column_name].quantile(0.25)
    q3 = df[column_name].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return df[column_name].between(lower_bound, upper_bound) | df[column_name].isna()


def remove_outliers_across_slope_features(df: pd.DataFrame, slope_features: list[str]) -> pd.DataFrame:
    """
    Remove rows that are outliers in any slope feature using the IQR rule.
    """
    cleaned_df = df.copy()

    for column_name in slope_features:
        mask = get_non_outlier_mask(cleaned_df, column_name)
        cleaned_df = cleaned_df[mask].copy()

    return cleaned_df


def main() -> None:
    data = load_csv(FINAL_DATA_VISIT_TO_VISIT_FILE)
    data = prepare_data(data)

    slope_features = get_slope_features(data)

    cleaned_data = remove_outliers_across_slope_features(data, slope_features)

    save_csv(cleaned_data, FINAL_DATA_WITHOUT_SLOPE_OUTLIERS_FILE)

    print("Slope features found:", slope_features)
    print("Original shape:", data.shape)
    print("Cleaned shape:", cleaned_data.shape)
    print("Output saved to:", FINAL_DATA_WITHOUT_SLOPE_OUTLIERS_FILE)


if __name__ == "__main__":
    main()