from pathlib import Path
import pandas as pd
from src.config import (
    VISIT_FILE,
    WEEKS_FILE,
    DATE_COLUMN,
    COMMON_COLUMNS,
    DATE_FORMAT,
)


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

def convert_date_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Convert the specified column to datetime."""
    df = df.copy()
    df[column_name] = pd.to_datetime(
        df[column_name],
        format=DATE_FORMAT,
        errors="raise",
    )
    return df

def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return a copy of the DataFrame with only the required columns."""
    return df[columns].copy()

def find_extra_rows(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    join_columns: list[str],
) -> pd.DataFrame:
    """
    Find rows that exist in right_df but not in left_df,
    based on the specified join columns.
    """
    merged_df = left_df.merge(
        right_df,
        how="right",
        on=join_columns,
        indicator=True,
    )
    return merged_df.loc[merged_df["_merge"] != "both"].copy()


def main() -> None:
    visit_data = load_csv(VISIT_FILE)
    weeks_data = load_csv(WEEKS_FILE)

    print("visit_to_visit columns:")
    print(visit_data.columns.tolist())

    print("\n5_weeks_without_missing columns:")
    print(weeks_data.columns.tolist())

    print("\nvisit_to_visit shape:", visit_data.shape)
    print("5_weeks_without_missing shape:", weeks_data.shape)

    visit_data = convert_date_column(visit_data, DATE_COLUMN)
    weeks_data = convert_date_column(weeks_data, DATE_COLUMN)

    visit_data = select_columns(visit_data, COMMON_COLUMNS)
    weeks_data = select_columns(weeks_data, COMMON_COLUMNS)

    extra_rows = find_extra_rows(visit_data, weeks_data, COMMON_COLUMNS)

    print("\nExtra rows shape:", extra_rows.shape)
    print("\nExtra rows preview:")
    print(extra_rows.head())


if __name__ == "__main__":
    main()