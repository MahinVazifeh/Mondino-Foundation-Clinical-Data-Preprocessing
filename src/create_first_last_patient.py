from pathlib import Path

import pandas as pd

from src.config import (
    UPDATED_MS_FILE,
    PATIENT_CAP_FILE,
    ONSET_DATE_FILE,
    FIRST_LAST_PATIENT_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    DATE_OF_BIRTH_COLUMN,
    DATE_OF_ONSET_COLUMN,
    CAP_COLUMN,
    DATE_FORMAT,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def prepare_clinical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Convert visit date column to datetime."""
    df = df.copy()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format=DATE_FORMAT, errors="raise")
    return df


def merge_patient_cap(clinical_df: pd.DataFrame, cap_df: pd.DataFrame) -> pd.DataFrame:
    """Merge clinical data with CAP data."""
    merged_df = clinical_df.merge(
        cap_df,
        left_on=PATIENT_ID_COLUMN,
        right_on="Paziente ID",
        how="left",
    )
    return merged_df


def merge_onset_data(clinical_df: pd.DataFrame, onset_df: pd.DataFrame) -> pd.DataFrame:
    """Merge clinical data with onset date data."""
    merged_df = clinical_df.merge(
        onset_df,
        left_on=PATIENT_ID_COLUMN,
        right_on="Patient_id",
        how="left",
    )
    return merged_df


def clean_merged_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean columns, convert types, and remove rows with missing CAP."""
    df = df.copy()

    df = df.drop(columns=["Paziente ID", "Patient_id"], errors="ignore")

    df = df.rename(
        columns={
            "Data di nascita": DATE_OF_BIRTH_COLUMN,
            "Onset_date": DATE_OF_ONSET_COLUMN,
        }
    )

    df = df.dropna(subset=[CAP_COLUMN])

    df[DATE_OF_ONSET_COLUMN] = pd.to_datetime(
        df[DATE_OF_ONSET_COLUMN],
        format=DATE_FORMAT,
        errors="raise",
    )

    df[CAP_COLUMN] = df[CAP_COLUMN].astype(int)

    return df


def get_first_and_last_visits(df: pd.DataFrame) -> pd.DataFrame:
    """Return the first and last visit row for each patient."""
    first_visits = df.groupby(PATIENT_ID_COLUMN).head(1)
    last_visits = df.groupby(PATIENT_ID_COLUMN).tail(1)

    result_df = (
        pd.concat([first_visits, last_visits])
        .drop_duplicates()
        .sort_values(by=[PATIENT_ID_COLUMN, DATE_COLUMN])
    )

    selected_columns = [
        PATIENT_ID_COLUMN,
        CAP_COLUMN,
        DATE_OF_BIRTH_COLUMN,
        DATE_OF_ONSET_COLUMN,
        DATE_COLUMN,
    ]
    return result_df[selected_columns].copy()


def add_first_and_last_visit_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Add first and last visit dates for each patient."""
    grouped_dates = (
        df.groupby(PATIENT_ID_COLUMN)[DATE_COLUMN]
        .agg(
            First_Date_of_visit="min",
            Last_Date_of_visit="max",
        )
        .reset_index()
    )

    merged_df = df.merge(
        grouped_dates,
        on=PATIENT_ID_COLUMN,
        how="left",
    )

    result_df = merged_df.groupby(PATIENT_ID_COLUMN).head(1).reset_index(drop=True)
    return result_df


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def main() -> None:
    clinical_df = load_csv(UPDATED_MS_FILE)
    cap_df = load_csv(PATIENT_CAP_FILE)
    onset_df = load_csv(ONSET_DATE_FILE)

    clinical_df = prepare_clinical_data(clinical_df)
    merged_df = merge_patient_cap(clinical_df, cap_df)
    merged_df = merge_onset_data(merged_df, onset_df)
    merged_df = clean_merged_data(merged_df)

    first_last_visits_df = get_first_and_last_visits(merged_df)
    output_df = add_first_and_last_visit_dates(first_last_visits_df)

    output_columns = [
        PATIENT_ID_COLUMN,
        CAP_COLUMN,
        DATE_OF_BIRTH_COLUMN,
        DATE_OF_ONSET_COLUMN,
        "First_Date_of_visit",
        "Last_Date_of_visit",
    ]

    save_csv(output_df[output_columns], FIRST_LAST_PATIENT_FILE)

    print("Output saved to:", FIRST_LAST_PATIENT_FILE)
    print("Output shape:", output_df[output_columns].shape)
    print(output_df[output_columns].head())


if __name__ == "__main__":
    main()