import numpy as np
import pandas as pd
import mssev as ms

from src.config import (
    COMPLETE_CLINICAL_DATA_FILE,
    FIRST_LAST_PATIENT_FILE,
    COMPLETED_DATA_WITH_PROGRESSION_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    DATE_OF_ONSET_COLUMN,
    EDSS_COLUMN,
    MSSS_COLUMN,
    MSSS_CLASSIFIED_COLUMN,
    NUM_OBS_COLUMN,
    DIFF_EDSS_COLUMN,
    OUTCOME_COLUMN,
    YEAR_FROM_ONSET_COLUMN,
    PATIENT_NUMBER_COLUMN,
    DATE_FORMAT,
)


MSSS_BINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
MSSS_LABELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def load_csv(file_path) -> pd.DataFrame:
    """Load dataset from CSV."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path) -> None:
    """Save DataFrame to CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def add_msss_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Compute MSSS and MSSS classes."""
    df = df.copy()

    df[MSSS_COLUMN] = ms.MSSS(
        df,
        ds=EDSS_COLUMN,
        duration="num_year_from_onset",
    )

    df = df.dropna(subset=[MSSS_COLUMN]).copy()

    df[MSSS_CLASSIFIED_COLUMN] = pd.cut(
        df[MSSS_COLUMN],
        bins=MSSS_BINS,
        labels=MSSS_LABELS,
        include_lowest=True,
        right=True,
    )

    return df


def classify_outcome(diff_value: float) -> str:
    """Map EDSS difference to a progression category."""
    if pd.isnull(diff_value):
        return "First obs"
    if diff_value == 0.5:
        return "Very Mild Progression"
    if diff_value == 1:
        return "Mild progression"
    if diff_value == 1.5:
        return "Moderate progression"
    if diff_value < 0:
        return "Improvement"
    if diff_value == 0:
        return "No change"
    return "Severe Progression"


def add_outcome_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Create outcome feature from EDSS differences between visits."""
    df = df.copy()

    df[NUM_OBS_COLUMN] = df.groupby(PATIENT_ID_COLUMN)[PATIENT_ID_COLUMN].transform("count")
    df = df[df[NUM_OBS_COLUMN] > 1].copy()

    df = df.sort_values(by=[PATIENT_ID_COLUMN, DATE_COLUMN]).copy()

    df[DIFF_EDSS_COLUMN] = df.groupby(PATIENT_ID_COLUMN)[EDSS_COLUMN].diff()

    df[OUTCOME_COLUMN] = df[DIFF_EDSS_COLUMN].map(classify_outcome)
    df[OUTCOME_COLUMN] = df[OUTCOME_COLUMN].map(
        {
            "First obs": 0,
            "Improvement": 1,
            "Very Mild Progression": 1,
            "Mild progression": 2,
            "Moderate progression": 3,
            "No change": 4,
            "Severe Progression": 5,
        }
    )

    return df


def merge_patient_level_features(
    clinical_df: pd.DataFrame,
    patient_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge patient-level features into the clinical dataset."""
    return clinical_df.merge(
        patient_df,
        on=PATIENT_ID_COLUMN,
        how="left",
    )


def add_year_from_onset(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-from-onset feature in years."""
    df = df.copy()

    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format=DATE_FORMAT, errors="raise")
    df[DATE_OF_ONSET_COLUMN] = pd.to_datetime(
        df[DATE_OF_ONSET_COLUMN],
        format=DATE_FORMAT,
        errors="raise",
    )

    df[YEAR_FROM_ONSET_COLUMN] = (
        (df[DATE_COLUMN] - df[DATE_OF_ONSET_COLUMN]).dt.days / 365.25
    ).round(2)

    return df


def add_patient_number(df: pd.DataFrame) -> pd.DataFrame:
    """Create sequential patient number."""
    df = df.copy()
    df[PATIENT_NUMBER_COLUMN] = df.groupby(PATIENT_ID_COLUMN).ngroup() + 1
    return df


def main() -> None:
    clinical_df = load_csv(COMPLETE_CLINICAL_DATA_FILE)
    first_last_df = load_csv(FIRST_LAST_PATIENT_FILE)

    clinical_df = add_msss_feature(clinical_df)
    clinical_df = add_outcome_feature(clinical_df)
    clinical_df = merge_patient_level_features(clinical_df, first_last_df)
    clinical_df = add_year_from_onset(clinical_df)
    clinical_df = add_patient_number(clinical_df)

    save_csv(clinical_df, COMPLETED_DATA_WITH_PROGRESSION_FILE)

    print("Output saved to:", COMPLETED_DATA_WITH_PROGRESSION_FILE)
    print("Final shape:", clinical_df.shape)
    print(clinical_df.head())


if __name__ == "__main__":
    main()