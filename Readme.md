# 🧪 Clinical Data Processing, Fondazione Mondino IRCCS, Pavia

This repository offers a structured collection of **Jupyter notebooks** designed for comprehensive **clinical data processing**. Its functionalities encompass:

* **Data Preprocessing**: Cleaning, transforming, and preparing raw clinical data for analysis.
* **Feature Engineering**: Creating new, informative features from existing data to enhance model performance.
* **Quality Control**: Implementing checks and procedures to ensure data accuracy and reliability.

The tools within this repository are specifically tailored for **longitudinal data analysis**, with a particular emphasis on **disease progression modeling**. A prime example of its application is in understanding and predicting the progression of diseases like **Multiple Sclerosis (MS)**.

## 📌 Overview

This project includes a modular pipeline for:

* **🧬 Selecting and generating important clinical features**
* **🧹 Cleaning data and removing outliers**
* **📅 Extracting time-based features**
* **📈 Tracking clinical progression metrics** (e.g., MSSS)
* **🎯 Normalizing scores and rounding values**
* **✅ Ensuring data quality and consistency**

Each notebook is designed to work independently or as part of a full pipeline.

## 📂 Scripts Included

### 🔧 Core Preprocessing & Feature Engineering

| Num | Notebook                                      | Description                                                               |
| :-- | :-------------------------------------------- | :------------------------------------------------------------------------ |
| 1   | `Select_Important_Features_From_Original.ipynb` | Selects key clinical features from the original dataset.                  |
| 1.5 | `Update_Original_Data.ipynb`                  | Updates the original data with newly derived or cleaned fields.           |
| 2   | `Year_Month_DateOfVisit.ipynb`                | Extracts year and month from visit dates.                                 |
| 3   | `Relapse_Feature.ipynb`                       | Creates a binary relapse indicator per visit.                             |
| 4   | `Treatment.ipynb`                             | Encodes treatment information and relevant interventions.                 |
| 5   | `MSSS_Progression_Features.ipynb`             | Creates progression-related MSSS features.                                |
| 6   | `Delete_Duplicate_Age_at_Visit_Date.ipynb`    | Removes duplicated age and visit date records.                            |
| 7   | `MSSS_Score.ipynb`                            | Computes the Multiple Sclerosis Severity Score (MSSS).                    |
| 8   | `Feature_Selection_for_MSSS_Data_Visualization.ipynb` | Filters features for better MSSS visualization.                           |
| 9   | `Season_Feature_Generation.ipynb`             | Adds seasonal context (Spring, Summer, etc.) to visits.                   |
| 10  | `Outlier_Detection.ipynb`                     | Identifies and flags statistical outliers.                                |
| 11  | `Round_SubScores.ipynb`                       | Rounds sub-scores for standardized representation.                        |
