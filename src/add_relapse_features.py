from pathlib import Path

import pandas as pd

from src.config import (
    UPDATED_MS_INPUT_FILE,
    RELAPSE_SOURCE_FILE,
    UPDATED_MS_WITH_RELAPSE_FILE,
    RELAPSE_PROCESSED_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    RELAPSE_PATIENT_ID_COLUMN,
    RELAPSE_DATE_COLUMN,
    RELAPSE_COUNT_COLUMN,
    RELAPSE_NUMBER_COLUMN,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_relapse_data(relapse_df: pd.DataFrame) -> pd.DataFrame:
    """Sort relapse data and create cumulative relapse counts per patient."""
    relapse_df = relapse_df.copy()
    relapse_df[RELAPSE_DATE_COLUMN] = pd.to_datetime(
        relapse_df[RELAPSE_DATE_COLUMN],
        errors="raise",
    )

    relapse_df = relapse_df.sort_values(
        by=[RELAPSE_PATIENT_ID_COLUMN, RELAPSE_DATE_COLUMN]
    ).reset_index(drop=True)

    relapse_df[RELAPSE_COUNT_COLUMN] = (
        relapse_df.groupby(RELAPSE_PATIENT_ID_COLUMN).cumcount() + 1
    )

    return relapse_df


def prepare_clinical_data(clinical_df: pd.DataFrame) -> pd.DataFrame:
    """Convert visit date column to datetime."""
    clinical_df = clinical_df.copy()
    clinical_df[DATE_COLUMN] = pd.to_datetime(
        clinical_df[DATE_COLUMN],
        errors="raise",
    )
    return clinical_df


def count_relapses_until_visit(
    clinical_df: pd.DataFrame,
    relapse_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add cumulative relapse count up to each visit date for each patient.
    """
    clinical_df = clinical_df.copy()
    clinical_df[RELAPSE_NUMBER_COLUMN] = 0

    relapse_lookup = {
        patient_id: patient_relapses[[RELAPSE_DATE_COLUMN, RELAPSE_COUNT_COLUMN]].reset_index(
            drop=True
        )
        for patient_id, patient_relapses in relapse_df.groupby(RELAPSE_PATIENT_ID_COLUMN)
    }

    relapse_counts = []

    for _, row in clinical_df.iterrows():
        patient_id = row[PATIENT_ID_COLUMN]
        visit_date = row[DATE_COLUMN]

        if patient_id not in relapse_lookup:
            relapse_counts.append(0)
            continue

        patient_relapses = relapse_lookup[patient_id]
        past_relapses = patient_relapses[
            patient_relapses[RELAPSE_DATE_COLUMN] <= visit_date
        ]

        if past_relapses.empty:
            relapse_counts.append(0)
        else:
            relapse_counts.append(int(past_relapses.iloc[-1][RELAPSE_COUNT_COLUMN]))

    clinical_df[RELAPSE_NUMBER_COLUMN] = relapse_counts
    return clinical_df


def main() -> None:
    clinical_df = load_csv(UPDATED_MS_INPUT_FILE)
    relapse_df = load_csv(RELAPSE_SOURCE_FILE)

    clinical_df = prepare_clinical_data(clinical_df)
    relapse_df = prepare_relapse_data(relapse_df)

    updated_clinical_df = count_relapses_until_visit(clinical_df, relapse_df)

    save_csv(relapse_df, RELAPSE_PROCESSED_FILE)
    save_csv(updated_clinical_df, UPDATED_MS_WITH_RELAPSE_FILE)

    print("Processed relapse file saved to:", RELAPSE_PROCESSED_FILE)
    print("Updated clinical file saved to:", UPDATED_MS_WITH_RELAPSE_FILE)
    print("Final shape:", updated_clinical_df.shape)
    print(updated_clinical_df.head())


if __name__ == "__main__":
    main()