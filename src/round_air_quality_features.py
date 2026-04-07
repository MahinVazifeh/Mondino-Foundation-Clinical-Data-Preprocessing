from pathlib import Path
import math

import pandas as pd

from src.config import AIR_FS_FILE, ROUNDED_AIR_FS_FILE


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load dataset from CSV."""
    return pd.read_csv(file_path)


def save_csv(df: pd.DataFrame, file_path: Path) -> None:
    """Save DataFrame to CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def round_to_nearest(value: float):
    """Custom rounding function."""
    if pd.isna(value):
        return value

    difference_ceil = math.ceil(value) - value

    if difference_ceil <= 0.25:
        return math.ceil(value)
    elif difference_ceil <= 0.75:
        return math.ceil(value) - 0.5
    else:
        return math.floor(value)


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select relevant columns."""
    return df.iloc[:, 2:10].copy()


def apply_rounding(df: pd.DataFrame) -> pd.DataFrame:
    """Apply rounding function to all values."""
    return df.applymap(round_to_nearest)


def main() -> None:
    dataset = load_csv(AIR_FS_FILE)

    dataset = select_columns(dataset)
    dataset = apply_rounding(dataset)

    save_csv(dataset, ROUNDED_AIR_FS_FILE)

    print("Output saved to:", ROUNDED_AIR_FS_FILE)
    print("Shape:", dataset.shape)
    print(dataset.head())


if __name__ == "__main__":
    main()