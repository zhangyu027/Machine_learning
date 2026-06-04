import pandas as pd

def build_feature_frame(gold_df):
    df = gold_df.copy()
    df["note_length"] = df["clinical_note"].fillna("").str.len()
    df["is_high_glucose"] = (df["glucose"] > 180).astype(int)
    df["is_low_spo2"] = (df["spo2_min"] < 92).astype(int)
    df["age_x_los"] = df["age"] * df["length_of_stay"]
    return pd.get_dummies(
        df[[
            "age", "length_of_stay", "creatinine", "wbc", "glucose", "hemoglobin",
            "heart_rate_mean", "spo2_min", "systolic_bp_mean", "temperature_max",
            "note_length", "is_high_glucose", "is_low_spo2", "age_x_los",
            "sex", "race_group", "payer", "diagnosis_group", "image_modality",
            "readmitted_30d"
        ]],
        columns=["sex", "race_group", "payer", "diagnosis_group", "image_modality"],
        drop_first=True,
    )
