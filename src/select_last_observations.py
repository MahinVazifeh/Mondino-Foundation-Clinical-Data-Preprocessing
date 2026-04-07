from pathlib import Path

import pandas as pd

from src.config import (
    UPDATED_MS_FILE,
    TEN_OBS_OUTPUT_FILE,
    PATIENT_ID_COLUMN,
    MIN_OBSERVATIONS_PER_PATIENT,
)


def load_data(file_path: Path) -> pd.DataFrame:
    """Load dataset from CSV."""
    return pd.read_csv(file_path)


def filter_patients_with_min_records(
    df: pd.DataFrame,
    patient_column: str,
    min_records: int,
) -> pd.DataFrame:
    """Keep only patients with at least `min_records` observations."""
    valid_ids = (
        df.groupby(patient_column)
        .filter(lambda x: len(x) >= min_records)[patient_column]
        .unique()
    )

    return df[df[patient_column].isin(valid_ids)].copy()


def get_last_n_records_per_patient(
    df: pd.DataFrame,
    patient_column: str,
    n: int,
) -> pd.DataFrame:
    """Return the last `n` records per patient."""
    return df.groupby(patient_column).tail(n).copy()


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save DataFrame to CSV (create folder if needed)."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def main() -> None:
    df = load_data(UPDATED_MS_FILE)

    print("Original shape:", df.shape)

    filtered_df = filter_patients_with_min_records(
        df,
        PATIENT_ID_COLUMN,
        MIN_OBSERVATIONS_PER_PATIENT,
    )

    result_df = get_last_n_records_per_patient(
        filtered_df,
        PATIENT_ID_COLUMN,
        MIN_OBSERVATIONS_PER_PATIENT,
    )

    print("Filtered shape:", result_df.shape)

    save_csv(result_df, TEN_OBS_OUTPUT_FILE)

    print("Saved to:", TEN_OBS_OUTPUT_FILE)
    print(result_df.head())


if __name__ == "__main__":
    main()