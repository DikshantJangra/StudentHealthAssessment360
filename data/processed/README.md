# Processed Data Documentation

## Overview
This folder contains the **machine-readable** version of the student health dataset after preprocessing and feature engineering.

**Notebook:** [Data Preprocessing & EDA](https://colab.research.google.com/drive/1mzHsZ85XsmSOWcDOzpGTqQdcqMXKR1yC?usp=sharing)

---

## Transformation Summary

### Input → Output
- **Original Data:** 1000 rows × 14 columns  
- **Cleaned Data:** 1000 rows × 16 columns  
- **Change:** Dropped `Student_ID`, expanded categorical features via One-Hot Encoding

### Exploratory Data Analysis
![EDA Results](EDA_results.png)

---

## Processing Pipeline

### 1. **Data Cleaning**
- Removed `Student_ID` (non-predictive identifier)
- Handled missing values and outliers
- Capped extreme values in `Heart_Rate`, `BP_Systolic`, and `BP_Diastolic`

### 2. **Feature Encoding**

#### Ordinal Encoding (Preserves Order)
- **Physical_Activity:** Low → 0, Moderate → 1, High → 2
- **Sleep_Quality:** Poor → 0, Average → 1, Good → 2
- **Health_Risk_Level (Target):** Low → 0, Moderate → 1, High → 2

#### One-Hot Encoding (Categorical → Binary)
- **Gender:** `Gender_F`, `Gender_M`
- **Mood:** `Mood_Happy`, `Mood_Neutral`, `Mood_Stressed`

### 3. **Standard Scaling**
Applied to all continuous numerical features:
- `Age`, `Heart_Rate`, `BP_Systolic`, `BP_Diastolic`
- `Stress_Bio`, `Stress_Self`, `Study_Hours`, `Project_Hours`

**Effect:** Transforms values to have Mean = 0, Std Dev = 1  
**Range:** Most values fall between -3.0 and 3.0  
**Interpretation:** 0 = Average, +2 = Significantly Above Average, -2 = Significantly Below Average

---

## Final Schema

| Column Name | Type | Format | Example |
|-------------|------|--------|---------|
| Age | Numerical | Scaled | 0.45 |
| Heart_Rate | Numerical | Scaled & Capped | -1.22 |
| BP_Systolic | Numerical | Scaled & Capped | 0.15 |
| BP_Diastolic | Numerical | Scaled & Capped | -0.89 |
| Stress_Bio | Numerical | Scaled | 1.10 |
| Stress_Self | Numerical | Scaled | -0.40 |
| Study_Hours | Numerical | Scaled | 1.56 |
| Project_Hours | Numerical | Scaled | -0.20 |
| Physical_Activity | Ordinal | 0, 1, 2 | 2 |
| Sleep_Quality | Ordinal | 0, 1, 2 | 0 |
| Gender_F | Binary | 0 or 1 | 1 |
| Gender_M | Binary | 0 or 1 | 0 |
| Mood_Happy | Binary | 0 or 1 | 0 |
| Mood_Neutral | Binary | 0 or 1 | 1 |
| Mood_Stressed | Binary | 0 or 1 | 0 |
| **Health_Risk_Level** | **Target** | **0, 1, 2** | **1** |

---

## Model Input Specification

**Features:** 15 columns (all except `Health_Risk_Level`)  
**Target:** 1 column (`Health_Risk_Level`)  
**Task:** Multi-class classification (3 classes: Low, Moderate, High)

---

## Why These Transformations?

### Standard Scaling
Prevents features with larger numerical ranges (e.g., Blood Pressure ~120) from dominating smaller features (e.g., Stress Level ~3). Ensures equal weighting in ML models.

### One-Hot Encoding
Prevents the model from assuming ordinal relationships in nominal categories. "Happy" is not mathematically "less than" "Stressed" — they are independent states.

### Ordinal Encoding
Preserves meaningful order in features like Sleep Quality (Poor < Average < Good) and Physical Activity (Low < Moderate < High).

---

## Files in This Directory

- `cleaned_student_data.csv` - Final processed dataset ready for ML training
- `README.md` - This documentation file

---

## Next Steps

This processed data is consumed by:
1. **ML Training Pipeline** (`notebooks/02_dikshant_training.ipynb`)
2. **Prediction Engine** (`src/ml_engine/predictor.py`)
3. **Streamlit UI** (`src/ui/app.py`)

---

**Processed by:** Ashish (EDA & Feature Engineering)