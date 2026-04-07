from pathlib import Path

import pandas as pd

from src.config import (
    ONSET_DATE_FILE,
    UPDATED_MS_WITH_RELAPSE_AGE_FILE,
    DATA_WITH_DISEASE_DURATION_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    DATE_OF_ONSET_COLUMN,
    RAW_PATIENT_ID_COLUMN,
    RAW_ONSET_DATE_COLUMN,
    DISEASE_DURATION_WEEKS_COLUMN,
    DIFF_YEAR_COLUMN,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_main_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    df[PATIENT_ID_COLUMN] = df[PATIENT_ID_COLUMN].astype(str)
    return df


def prepare_onset_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[RAW_PATIENT_ID_COLUMN] = df[RAW_PATIENT_ID_COLUMN].astype(str)
    df[RAW_ONSET_DATE_COLUMN] = pd.to_datetime(
        df[RAW_ONSET_DATE_COLUMN],
        errors="coerce",
    )

    df = df.rename(
        columns={
            RAW_ONSET_DATE_COLUMN: DATE_OF_ONSET_COLUMN,
        }
    )

    return df


def merge_onset_data(main_df: pd.DataFrame, onset_df: pd.DataFrame) -> pd.DataFrame:
    merged_df = main_df.merge(
        onset_df[[RAW_PATIENT_ID_COLUMN, DATE_OF_ONSET_COLUMN]],
        left_on=PATIENT_ID_COLUMN,
        right_on=RAW_PATIENT_ID_COLUMN,
        how="left",
    )

    return merged_df.drop(columns=[RAW_PATIENT_ID_COLUMN], errors="ignore")


def add_disease_duration_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[DATE_OF_ONSET_COLUMN] = pd.to_datetime(df[DATE_OF_ONSET_COLUMN], errors="coerce")

    df[DISEASE_DURATION_WEEKS_COLUMN] = (
        (df[DATE_COLUMN] - df[DATE_OF_ONSET_COLUMN]).dt.days / 7
    ).round().astype("Int64")

    df[DIFF_YEAR_COLUMN] = (
        (df[DATE_COLUMN] - df[DATE_OF_ONSET_COLUMN]).dt.days / 365.25
    ).round(3)

    return df


def main() -> None:
    main_df = load_csv(UPDATED_MS_WITH_RELAPSE_AGE_FILE)
    onset_df = load_csv(ONSET_DATE_FILE)

    main_df = prepare_main_data(main_df)
    onset_df = prepare_onset_data(onset_df)

    merged_df = merge_onset_data(main_df, onset_df)
    merged_df = add_disease_duration_features(merged_df)

    save_csv(merged_df, DATA_WITH_DISEASE_DURATION_FILE)

    print("Output saved to:", DATA_WITH_DISEASE_DURATION_FILE)
    print("Final shape:", merged_df.shape)
    print(merged_df.head())


if __name__ == "__main__":
    main()