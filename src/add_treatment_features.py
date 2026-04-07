from pathlib import Path

import pandas as pd

from src.config import (
    FOUR_WEEKS_DATA_FILE,
    TREATMENT_SOURCE_FILE,
    DATA_WITH_TREATMENT_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    DATE_FORMAT,
    TREATMENT_PATIENT_ID_COLUMN,
    TREATMENT_START_DATE_COLUMN,
    TREATMENT_END_DATE_COLUMN,
    MS_FIRST_LINE_COLUMN,
    MS_SECOND_LINE_COLUMN,
    MS_OTHER_COLUMN,
)


BETWEEN_VISITS_FIRST_LINE_COLUMN = "First_line_Treat_between_visits"
BETWEEN_VISITS_SECOND_LINE_COLUMN = "Second_line_Treat_between_visits"
BETWEEN_VISITS_OTHER_LINE_COLUMN = "Other_line_Treat_between_visits"

PREVIOUS_4_WEEKS_FIRST_LINE_COLUMN = "First_line_Treat_previous_4_weeks"
PREVIOUS_4_WEEKS_SECOND_LINE_COLUMN = "Second_line_Treat_previous_4_weeks"
PREVIOUS_4_WEEKS_OTHER_LINE_COLUMN = "Other_line_Treat_previous_4_weeks"


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_clinical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Convert visit date column to datetime and sort data."""
    df = df.copy()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format=DATE_FORMAT, errors="raise")
    df = df.sort_values(by=[PATIENT_ID_COLUMN, DATE_COLUMN]).reset_index(drop=True)
    return df


def prepare_treatment_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and convert treatment data."""
    df = df.copy()

    df = df[~df[TREATMENT_PATIENT_ID_COLUMN].astype(str).str.contains("TUR_MS", na=False)]
    df[TREATMENT_PATIENT_ID_COLUMN] = df[TREATMENT_PATIENT_ID_COLUMN].astype("int64")

    df[TREATMENT_START_DATE_COLUMN] = pd.to_datetime(
        df[TREATMENT_START_DATE_COLUMN],
        format=DATE_FORMAT,
        errors="raise",
    )
    df[TREATMENT_END_DATE_COLUMN] = pd.to_datetime(
        df[TREATMENT_END_DATE_COLUMN],
        format=DATE_FORMAT,
        errors="raise",
    )

    return df


def initialize_treatment_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create treatment feature columns initialized to zero."""
    df = df.copy()

    for column in [
        BETWEEN_VISITS_FIRST_LINE_COLUMN,
        BETWEEN_VISITS_SECOND_LINE_COLUMN,
        BETWEEN_VISITS_OTHER_LINE_COLUMN,
        PREVIOUS_4_WEEKS_FIRST_LINE_COLUMN,
        PREVIOUS_4_WEEKS_SECOND_LINE_COLUMN,
        PREVIOUS_4_WEEKS_OTHER_LINE_COLUMN,
    ]:
        df[column] = 0

    return df


def add_between_visit_treatment_features(
    clinical_df: pd.DataFrame,
    treatment_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add treatment counts that occurred between one visit and the next visit
    for the same patient.
    """
    clinical_df = clinical_df.copy()
    treatment_patient_ids = set(treatment_df[TREATMENT_PATIENT_ID_COLUMN].unique())

    for index in range(len(clinical_df) - 1):
        current_row = clinical_df.iloc[index]
        next_row = clinical_df.iloc[index + 1]

        patient_id = current_row[PATIENT_ID_COLUMN]
        visit_date = current_row[DATE_COLUMN]

        if next_row[PATIENT_ID_COLUMN] != patient_id:
            continue

        next_visit_date = next_row[DATE_COLUMN]

        if patient_id not in treatment_patient_ids:
            continue

        matching_rows = treatment_df[
            (treatment_df[TREATMENT_PATIENT_ID_COLUMN] == patient_id)
            & (treatment_df[TREATMENT_START_DATE_COLUMN] >= visit_date)
            & (treatment_df[TREATMENT_END_DATE_COLUMN] < next_visit_date)
        ].fillna(0)

        if not matching_rows.empty:
            clinical_df.loc[index + 1, BETWEEN_VISITS_FIRST_LINE_COLUMN] = matching_rows[
                MS_FIRST_LINE_COLUMN
            ].sum()
            clinical_df.loc[index + 1, BETWEEN_VISITS_SECOND_LINE_COLUMN] = matching_rows[
                MS_SECOND_LINE_COLUMN
            ].sum()
            clinical_df.loc[index + 1, BETWEEN_VISITS_OTHER_LINE_COLUMN] = matching_rows[
                MS_OTHER_COLUMN
            ].sum()

    return clinical_df


def add_previous_4_weeks_treatment_features(
    clinical_df: pd.DataFrame,
    treatment_df: pd.DataFrame,
) -> pd.DataFrame:
    """Add treatment counts for the 4 weeks before each visit."""
    clinical_df = clinical_df.copy()
    treatment_patient_ids = set(treatment_df[TREATMENT_PATIENT_ID_COLUMN].unique())

    for index, row in clinical_df.iterrows():
        patient_id = row[PATIENT_ID_COLUMN]
        visit_date = row[DATE_COLUMN]

        if patient_id not in treatment_patient_ids:
            continue

        start_window = visit_date - pd.DateOffset(weeks=4)

        matching_rows = treatment_df[
            (treatment_df[TREATMENT_PATIENT_ID_COLUMN] == patient_id)
            & (treatment_df[TREATMENT_START_DATE_COLUMN] >= start_window)
            & (treatment_df[TREATMENT_END_DATE_COLUMN] < visit_date)
        ].fillna(0)

        if not matching_rows.empty:
            clinical_df.loc[index, PREVIOUS_4_WEEKS_FIRST_LINE_COLUMN] = matching_rows[
                MS_FIRST_LINE_COLUMN
            ].sum()
            clinical_df.loc[index, PREVIOUS_4_WEEKS_SECOND_LINE_COLUMN] = matching_rows[
                MS_SECOND_LINE_COLUMN
            ].sum()
            clinical_df.loc[index, PREVIOUS_4_WEEKS_OTHER_LINE_COLUMN] = matching_rows[
                MS_OTHER_COLUMN
            ].sum()

    return clinical_df


def main() -> None:
    clinical_df = load_csv(FOUR_WEEKS_DATA_FILE)
    treatment_df = load_csv(TREATMENT_SOURCE_FILE)

    clinical_df = prepare_clinical_data(clinical_df)
    treatment_df = prepare_treatment_data(treatment_df)
    clinical_df = initialize_treatment_columns(clinical_df)

    clinical_df = add_between_visit_treatment_features(clinical_df, treatment_df)
    clinical_df = add_previous_4_weeks_treatment_features(clinical_df, treatment_df)

    save_csv(clinical_df, DATA_WITH_TREATMENT_FILE)

    print("Output saved to:", DATA_WITH_TREATMENT_FILE)
    print("Final shape:", clinical_df.shape)
    print(clinical_df.head())


if __name__ == "__main__":
    main()