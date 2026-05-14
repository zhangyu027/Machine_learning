from pathlib import Path
import numpy as np
import pandas as pd


NOTE_TEMPLATES = [
    "Patient reports shortness of breath and fatigue. Imaging suggests mild abnormality.",
    "Stable patient with normal imaging and no acute distress.",
    "Elevated inflammatory markers with worsening symptoms and abnormal scan.",
    "Patient has prior condition and borderline lab findings requiring monitoring.",
    "Clinical note indicates severe symptoms, high risk history, and abnormal imaging.",
    "Routine follow-up with stable vitals and reassuring clinical assessment.",
]


def generate_synthetic_healthcare_data(
    n_patients=2500,
    image_size=32,
    output_dir="data/raw",
    seed=42,
):
    rng = np.random.default_rng(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    patient_ids = [f"PATIENT_{i:05d}" for i in range(n_patients)]

    age = rng.normal(58, 17, n_patients).clip(18, 90)
    sex = rng.integers(0, 2, n_patients)
    prior_condition = rng.binomial(1, 0.35, n_patients)
    site_id = rng.integers(0, 4, n_patients)

    lab_crp = rng.gamma(2.0, 4.0, n_patients)
    lab_wbc = rng.normal(7.5, 2.5, n_patients).clip(2, 25)
    lab_creatinine = rng.normal(1.0, 0.35, n_patients).clip(0.4, 4.5)
    oxygen_saturation = rng.normal(96, 3.5, n_patients).clip(70, 100)

    imaging_signal = (
        0.02 * (age - 50)
        + 0.45 * prior_condition
        + 0.08 * lab_crp
        + 0.03 * (100 - oxygen_saturation)
        + rng.normal(0, 0.8, n_patients)
    )

    risk_score = (
        -3.0
        + 0.035 * age
        + 0.9 * prior_condition
        + 0.12 * lab_crp
        + 0.15 * np.maximum(lab_wbc - 10, 0)
        + 0.18 * np.maximum(95 - oxygen_saturation, 0)
        + 0.65 * imaging_signal
        + rng.normal(0, 0.9, n_patients)
    )

    risk_probability = 1 / (1 + np.exp(-risk_score))
    high_risk = (risk_probability > 0.5).astype(int)

    notes = []
    for i in range(n_patients):
        if high_risk[i] == 1:
            notes.append(rng.choice([NOTE_TEMPLATES[0], NOTE_TEMPLATES[2], NOTE_TEMPLATES[4]]))
        else:
            notes.append(rng.choice([NOTE_TEMPLATES[1], NOTE_TEMPLATES[3], NOTE_TEMPLATES[5]]))

    images = np.zeros((n_patients, 1, image_size, image_size), dtype="float32")
    for i in range(n_patients):
        base_noise = rng.normal(0.3, 0.12, (image_size, image_size))
        if high_risk[i] == 1:
            cx, cy = rng.integers(10, 22), rng.integers(10, 22)
            base_noise[cx-4:cx+4, cy-4:cy+4] += rng.normal(0.45, 0.08)
        images[i, 0] = np.clip(base_noise, 0, 1)

    df = pd.DataFrame({
        "patient_id": patient_ids,
        "age": age.round(1),
        "sex": sex,
        "prior_condition": prior_condition,
        "site_id": site_id,
        "lab_crp": lab_crp.round(3),
        "lab_wbc": lab_wbc.round(3),
        "lab_creatinine": lab_creatinine.round(3),
        "oxygen_saturation": oxygen_saturation.round(3),
        "clinical_note": notes,
        "risk_probability_true": risk_probability.round(4),
        "high_risk": high_risk,
    })

    df.to_csv(output_dir / "synthetic_multimodal_patients.csv", index=False)
    np.save(output_dir / "synthetic_images.npy", images)

    return df, images


if __name__ == "__main__":
    df, images = generate_synthetic_healthcare_data()
    print(df.shape, images.shape)
