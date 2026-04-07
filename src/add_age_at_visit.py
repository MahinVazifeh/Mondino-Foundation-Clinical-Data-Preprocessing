from pathlib import Path
import pandas as pd
from src.config import (
    PATIENT_CAP_FILE,
    UPDATED_MS_WITH_RELAPSE_FILE,
    COMPLETE_CLINICAL_DATA_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    AGE_COLUMN,
    DATE_OF_BIRTH_COLUMN,
    RAW_DATE_OF_BIRTH_COLUMN,
    RAW_CAP_PATIENT_ID_COLUMN,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_clinical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the clinical dataset."""
    df = df.copy()

    df = df.drop_duplicates(
        subset=[PATIENT_ID_COLUMN, DATE_COLUMN],
        keep="first",
        ignore_index=True,
    )

    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    df[PATIENT_ID_COLUMN] = df[PATIENT_ID_COLUMN].astype(str)

    return df


def prepare_birth_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare patient birth-date data."""
    df = df.copy()

    df[RAW_DATE_OF_BIRTH_COLUMN] = pd.to_datetime(
        df[RAW_DATE_OF_BIRTH_COLUMN],
        errors="coerce",
    )
    df[RAW_CAP_PATIENT_ID_COLUMN] = df[RAW_CAP_PATIENT_ID_COLUMN].astype(str)

    df = df.rename(columns={RAW_DATE_OF_BIRTH_COLUMN: DATE_OF_BIRTH_COLUMN})

    return df


def merge_birth_data(
    clinical_df: pd.DataFrame,
    birth_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge birth-date information into the clinical dataset."""
    merged_df = clinical_df.merge(
        birth_df[[RAW_CAP_PATIENT_ID_COLUMN, DATE_OF_BIRTH_COLUMN]],
        left_on=PATIENT_ID_COLUMN,
        right_on=RAW_CAP_PATIENT_ID_COLUMN,
        how="left",
    )

    merged_df = merged_df.drop(columns=[RAW_CAP_PATIENT_ID_COLUMN], errors="ignore")
    return merged_df


def calculate_age_at_visit(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate patient age at each visit."""
    df = df.copy()

    df[AGE_COLUMN] = (
        df[DATE_COLUMN].dt.year
        - df[DATE_OF_BIRTH_COLUMN].dt.year
        - (
            (df[DATE_COLUMN].dt.month < df[DATE_OF_BIRTH_COLUMN].dt.month)
            | (
                (df[DATE_COLUMN].dt.month == df[DATE_OF_BIRTH_COLUMN].dt.month)
                & (df[DATE_COLUMN].dt.day < df[DATE_OF_BIRTH_COLUMN].dt.day)
            )
        )
    ).astype("Int64")

    return df


def main() -> None:
    clinical_df = load_csv(UPDATED_MS_WITH_RELAPSE_FILE)
    birth_df = load_csv(PATIENT_CAP_FILE)

    clinical_df = prepare_clinical_data(clinical_df)
    birth_df = prepare_birth_data(birth_df)

    merged_df = merge_birth_data(clinical_df, birth_df)
    merged_df = calculate_age_at_visit(merged_df)

    save_csv(merged_df, COMPLETE_CLINICAL_DATA_FILE)

    print("Output saved to:", COMPLETE_CLINICAL_DATA_FILE)
    print("Final shape:", merged_df.shape)
    print(merged_df.head())


if __name__ == "__main__":
    main()