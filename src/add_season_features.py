from pathlib import Path

import pandas as pd

from src.config import (
    FINAL_DATA_VISIT_TO_VISIT_FILE,
    SPRING_DATA_FILE,
    SUMMER_DATA_FILE,
    FALL_DATA_FILE,
    WINTER_DATA_FILE,
    DATE_COLUMN,
    MSSS_COLUMN,
    SEASON_VISIT_COLUMN,
    DATE_FORMAT,
)


SEASON_MAPPING = {
    "Spring": 1,
    "Summer": 2,
    "Fall": 3,
    "Winter": 4,
}


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save a DataFrame to CSV, creating parent directories if needed."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataset for seasonal feature creation."""
    df = df.copy()
    df = df.dropna(subset=[MSSS_COLUMN]).copy()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format=DATE_FORMAT, errors="raise")
    return df


def get_season(month: int) -> str:
    """Return season name for a given month."""
    if month in [3, 4, 5]:
        return "Spring"
    if month in [6, 7, 8]:
        return "Summer"
    if month in [9, 10, 11]:
        return "Fall"
    return "Winter"


def add_season_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add season feature based on visit date."""
    df = df.copy()
    df[SEASON_VISIT_COLUMN] = df[DATE_COLUMN].dt.month.apply(get_season)
    return df


def split_by_season(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Split dataset into one DataFrame per season."""
    return {
        "Spring": df[df[SEASON_VISIT_COLUMN] == "Spring"].copy(),
        "Summer": df[df[SEASON_VISIT_COLUMN] == "Summer"].copy(),
        "Fall": df[df[SEASON_VISIT_COLUMN] == "Fall"].copy(),
        "Winter": df[df[SEASON_VISIT_COLUMN] == "Winter"].copy(),
    }


def encode_season_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Encode season names as numeric values."""
    df = df.copy()
    df[SEASON_VISIT_COLUMN] = df[SEASON_VISIT_COLUMN].map(SEASON_MAPPING)
    return df


def main() -> None:
    data = load_csv(FINAL_DATA_VISIT_TO_VISIT_FILE)
    data = prepare_data(data)
    data = add_season_feature(data)

    seasonal_data = split_by_season(data)

    save_csv(seasonal_data["Spring"], SPRING_DATA_FILE)
    save_csv(seasonal_data["Summer"], SUMMER_DATA_FILE)
    save_csv(seasonal_data["Fall"], FALL_DATA_FILE)
    save_csv(seasonal_data["Winter"], WINTER_DATA_FILE)

    encoded_data = encode_season_feature(data)

    print("Spring shape:", seasonal_data["Spring"].shape)
    print("Summer shape:", seasonal_data["Summer"].shape)
    print("Fall shape:", seasonal_data["Fall"].shape)
    print("Winter shape:", seasonal_data["Winter"].shape)
    print("\nEncoded data preview:")
    print(encoded_data[[DATE_COLUMN, SEASON_VISIT_COLUMN]].head())


if __name__ == "__main__":
    main()