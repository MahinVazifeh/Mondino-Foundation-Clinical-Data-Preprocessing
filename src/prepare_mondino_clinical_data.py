import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.config import (
    MONDINO_ORIGINAL_EXCEL_FILE,
    UPDATED_MS_MONDINO_FILE,
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    DATE_OF_BIRTH_COLUMN,
    DATE_OF_DEATH_COLUMN,
    EDSS_COLUMN,
    SEX_COLUMN,
    PEDIATRIC_MS_COLUMN,
    AGE_COLUMN,
)


VISITS_SHEET_NAME = "Visite"
DEMOGRAPHICS_SHEET_NAME = "Anagrafica"

SELECTED_COLUMNS = [
    "Id",
    "Paziente ID",
    "Data visita",
    "Piramidale",
    "Cerebellare",
    "Troncoencefalica",
    "Sensitiva",
    "Sfinteriche",
    "Visiva",
    "Mentali",
    "Deambulazione",
    "Punteggio EDSS valutato dal clinico",
    "Data di nascita",
    "Data di morte",
    "Sesso",
    "SM in età pedriatrica",
]

RENAMED_COLUMNS = {
    "Id": "Id",
    "Paziente ID": PATIENT_ID_COLUMN,
    "Data visita": DATE_COLUMN,
    "Piramidale": "Pyramidal",
    "Cerebellare": "Cerebellar",
    "Troncoencefalica": "Thronchioencephalic",
    "Sensitiva": "Sensitive",
    "Sfinteriche": "Sphincteric",
    "Visiva": "Visual",
    "Mentali": "Mental",
    "Deambulazione": "Deambulation",
    "Punteggio EDSS valutato dal clinico": EDSS_COLUMN,
    "Data di nascita": DATE_OF_BIRTH_COLUMN,
    "Data di morte": DATE_OF_DEATH_COLUMN,
    "Sesso": SEX_COLUMN,
    "SM in età pedriatrica": PEDIATRIC_MS_COLUMN,
}


def load_excel_sheet(file_path: str, sheet_name: str) -> pd.DataFrame:
    """Load one sheet from an Excel file."""
    return pd.read_excel(file_path, sheet_name=sheet_name)


def merge_clinical_sheets(
    visits_df: pd.DataFrame,
    demographics_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge visit and demographic data."""
    return visits_df.merge(
        demographics_df,
        how="left",
        on="Paziente ID",
    )


def select_and_rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select required columns and rename them to standardized names."""
    df = df[SELECTED_COLUMNS].copy()
    return df.rename(columns=RENAMED_COLUMNS)


def filter_missing_target(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing EDSS target."""
    return df[df[EDSS_COLUMN].notna()].copy()


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns to datetime."""
    df = df.copy()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    df[DATE_OF_BIRTH_COLUMN] = pd.to_datetime(df[DATE_OF_BIRTH_COLUMN], errors="coerce")
    df[DATE_OF_DEATH_COLUMN] = pd.to_datetime(df[DATE_OF_DEATH_COLUMN], errors="coerce")
    return df


def encode_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical columns as numeric values."""
    df = df.copy()

    sex_encoder = LabelEncoder()
    pediatric_encoder = LabelEncoder()

    df[SEX_COLUMN] = sex_encoder.fit_transform(df[SEX_COLUMN].astype(str))
    df[PEDIATRIC_MS_COLUMN] = pediatric_encoder.fit_transform(
        df[PEDIATRIC_MS_COLUMN].astype(str)
    )

    return df


def remove_low_quality_single_visit_patients(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove patients with exactly one visit when that row
    has at least 50% missing values.
    """
    df = df.copy()
    rows_to_drop = []

    for patient_id, patient_df in df.groupby(PATIENT_ID_COLUMN):
        if len(patient_df) == 1:
            missing_rate = (patient_df.isnull().sum(axis=1) / patient_df.shape[1]) * 100
            if missing_rate.iloc[0] >= 50:
                rows_to_drop.extend(patient_df.index.tolist())

    return df.drop(index=rows_to_drop).copy()


def add_age_column(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate age at visit."""
    df = df.copy()
    age = (
        df[DATE_COLUMN].dt.year
        - df[DATE_OF_BIRTH_COLUMN].dt.year
        - (
            (df[DATE_COLUMN].dt.month < df[DATE_OF_BIRTH_COLUMN].dt.month)
            | (
                (df[DATE_COLUMN].dt.month == df[DATE_OF_BIRTH_COLUMN].dt.month)
                & (df[DATE_COLUMN].dt.day < df[DATE_OF_BIRTH_COLUMN].dt.day)
            )
        )
    )
    df[AGE_COLUMN] = age.astype("Int64")
    return df


def save_csv(df: pd.DataFrame, output_file: str) -> None:
    """Save DataFrame to CSV."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)


def main() -> None:
    visits_df = load_excel_sheet(MONDINO_ORIGINAL_EXCEL_FILE, VISITS_SHEET_NAME)
    demographics_df = load_excel_sheet(MONDINO_ORIGINAL_EXCEL_FILE, DEMOGRAPHICS_SHEET_NAME)

    clinical_df = merge_clinical_sheets(visits_df, demographics_df)
    clinical_df = select_and_rename_columns(clinical_df)
    clinical_df = filter_missing_target(clinical_df)
    clinical_df = convert_date_columns(clinical_df)
    clinical_df = encode_categorical_columns(clinical_df)
    clinical_df = remove_low_quality_single_visit_patients(clinical_df)
    clinical_df = add_age_column(clinical_df)

    save_csv(clinical_df, UPDATED_MS_MONDINO_FILE)

    print("Output saved to:", UPDATED_MS_MONDINO_FILE)
    print("Final shape:", clinical_df.shape)
    print("Unique patients:", clinical_df[PATIENT_ID_COLUMN].nunique())
    print(clinical_df.head())


if __name__ == "__main__":
    main()