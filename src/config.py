from pathlib import Path

# =========================
# Project Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

SECOND_VERSION_DIR = DATA_DIR / "second_version"

# =========================
# Input Files
# =========================
VISIT_FILE = SECOND_VERSION_DIR / "visit_to_visit.csv"
WEEKS_FILE = SECOND_VERSION_DIR / "5_weeks_without_missing.csv"

RAW_MS_DATA_FILE = DATA_DIR / "Updated_MS_14000.csv"
COMPLETE_CLINICAL_DATA_FILE = DATA_DIR / "Complete_Clinical_Data_12000.csv"
FIRST_LAST_OBSERVATION_FILE = OUTPUT_DIR / "First_Last_Observation_Patient.csv"
PATIENT_CAP_FILE = DATA_DIR / "Patient_CAP.csv"
ONSET_DATE_FILE = DATA_DIR / "Onset_date.csv"

ORIGINAL_MS_EXCEL_FILE = DATA_DIR / "Original.xlsx"
MONDINO_MS_EXCEL_FILE = DATA_DIR / "MondinoOriginal.xlsx"

SHIFTED_DATA_FILE = DATA_DIR / "Shifted_data.csv"
RELAPSE_SOURCE_FILE = DATA_DIR / "relapse.csv"
UPDATED_MS_WITH_RELAPSE_FILE = OUTPUT_DIR / "Updated_MS_with_relapse.csv"

FOUR_WEEKS_DATA_FILE = DATA_DIR / "4_weeks_without_missing_onset.csv"
AIR_FS_FILE = DATA_DIR / "4Weeks_Merged_AirFS.csv"
TREATMENT_SOURCE_FILE = DATA_DIR / "MS_patients_meas3.csv"

FOURTH_VERSION_DIR = DATA_DIR / "fourth_version"
ONE_WEEK_DATA_FILE = FOURTH_VERSION_DIR / "1_weeks_without_missing_onset.csv"
FINAL_DATA_VISIT_TO_VISIT_FILE = DATA_DIR / "Final_data_visit_to_visit.csv"

FINAL_DATA_VISIT_TO_VISIT_FILE = DATA_DIR / "Final_data_visit_to_visit.csv"


# =========================
# Output Files
# =========================
CLEANED_MS_DATA_FILE = OUTPUT_DIR / "Updated_MS.csv"
FIRST_LAST_PATIENT_FILE = OUTPUT_DIR / "First_Last_Patient.csv"
TEN_OBS_OUTPUT_FILE = OUTPUT_DIR / "10_Observation_per_patients.csv"

MONDINO_MS_DATA_FILE = OUTPUT_DIR / "Updated_MS_Mondino.csv"
SHIFTED_DATA_WITH_TIME_FEATURES_FILE = OUTPUT_DIR / "Shifted_data_with_year_month_week_day.csv"
COMPLETED_DATA_WITH_PROGRESSION_FILE = OUTPUT_DIR / "Completed_data_with_Progression_Outcome.csv"
COMPLETE_CLINICAL_DATA_FILE = OUTPUT_DIR / "Complete_Clinical_Data_12000.csv"

RELAPSE_PROCESSED_FILE = OUTPUT_DIR / "relapse_with_counts.csv"
UPDATED_MS_WITH_RELAPSE_FILE = OUTPUT_DIR / "Updated_MS_with_relapse.csv"
UPDATED_MS_WITH_RELAPSE_AGE_FILE = OUTPUT_DIR / "Updated_MS_with_relapse_ageatvisitdate.csv"

DATA_WITH_TREATMENT_FILE = OUTPUT_DIR / "data_with_treatment.csv"
DATA_WITH_DISEASE_DURATION_FILE = OUTPUT_DIR / "Data_with_WHO_2.csv"

SPRING_DATA_FILE = OUTPUT_DIR / "Spring_data.csv"
SUMMER_DATA_FILE = OUTPUT_DIR / "Summer_data.csv"
FALL_DATA_FILE = OUTPUT_DIR / "Fall_data.csv"
WINTER_DATA_FILE = OUTPUT_DIR / "Winter_data.csv"

FINAL_DATA_WITHOUT_SLOPE_OUTLIERS_FILE = OUTPUT_DIR / "Final_data_without_slope_outliers.csv"

ROUNDED_AIR_FS_FILE = OUTPUT_DIR / "4Weeks_Merged_AirFS_rounded.csv"


# =========================
# Column Names
# =========================

# =========================
# Standard Column Names
# =========================
PATIENT_ID_COLUMN = "Patient_ID"
DATE_COLUMN = "Date_of_visit"
DATE_OF_BIRTH_COLUMN = "Date_of_birth"
DATE_OF_ONSET_COLUMN = "Date_of_Onset"
DATE_OF_DEATH_COLUMN = "Date_of_death"

EDSS_COLUMN = "EDSS_score_assessed_by_clinician"
CAP_COLUMN = "CAP"

FIRST_LINE_TREAT_COLUMN = "First_line_Treat"
SECOND_LINE_TREAT_COLUMN = "Second_line_Treat"
OTHER_LINE_TREAT_COLUMN = "Other_line_Treat"

SEX_COLUMN = "Sex"
PEDIATRIC_MS_COLUMN = "MS_in_pediatric_age"

AGE_COLUMN = "Age"

MSSS_COLUMN = "MSSS"
MSSS_CLASSIFIED_COLUMN = "MSSS_classified"

NUM_OBS_COLUMN = "num_obs"
DIFF_EDSS_COLUMN = "Diff_EDSS"
OUTCOME_COLUMN = "Outcome"

YEAR_FROM_ONSET_COLUMN = "year_from_onset"
PATIENT_NUMBER_COLUMN = "Patient_number"

SEASON_VISIT_COLUMN = "Season_visitdate"
SLOPE_FEATURE_KEYWORD = "Slope"

DISEASE_DURATION_WEEKS_COLUMN = "DiseaseDuration"
DIFF_YEAR_COLUMN = "diff_year"

# =========================
# Raw Dataset Column Names
# =========================

RAW_PATIENT_ID_COLUMN = "Patient_id"
RELAPSE_PATIENT_ID_COLUMN = "Paziente ID"

RAW_VISIT_DATE_COLUMN = "Data visita"
RAW_DATE_OF_BIRTH_COLUMN = "Data di nascita"
RAW_DATE_OF_DEATH_COLUMN = "Data di morte"
RAW_ONSET_DATE_COLUMN = "Onset_date"

TREATMENT_PATIENT_ID_COLUMN = "patient_id"
TREATMENT_START_DATE_COLUMN = "start_date"
TREATMENT_END_DATE_COLUMN = "end_date"
MS_FIRST_LINE_COLUMN = "ms_first_line"
MS_SECOND_LINE_COLUMN = "ms_second_line"
MS_OTHER_COLUMN = "ms_other"


# =========================
# Engineered Feature Columns
# =========================

YEAR_VISIT_COLUMN = "Year_visit"
OBSERVATION_TIMES_COLUMN = "Observation_times"

YEAR_DIFF_COLUMN = "year_diff_firstvisit"
MONTH_DIFF_COLUMN = "month_diff_firstvisit"
WEEK_DIFF_COLUMN = "week_diff_firstvisit"
DAY_DIFF_COLUMN = "day_diff_firstvisit"

RELAPSE_NUMBER_COLUMN = "relapse_number"
RELAPSE_COUNT_COLUMN = "Relapse_Count"
RELAPSE_DATE_COLUMN = "relapse"


# =========================
# Common Column Groups
# =========================

COMMON_COLUMNS = [
    PATIENT_ID_COLUMN,
    DATE_COLUMN,
    EDSS_COLUMN,
]

# =========================
# Parameters
# =========================

DATE_FORMAT = "%Y-%m-%d"

MIN_OBSERVATIONS_PER_PATIENT = 10
