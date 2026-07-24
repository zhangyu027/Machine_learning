# Data Dictionary

| Field | Layer | Description |
|---|---|---|
| patient_id | Bronze/Silver/Gold | Synthetic patient identifier |
| study_id | Bronze/Silver/Gold | Synthetic imaging study identifier |
| age | Bronze/Silver/Gold | Patient age |
| sex | Bronze/Silver | Source sex value |
| modality | Bronze/Silver | Imaging modality: XRay, CT, or MRI |
| scanner_site | Bronze/Silver | Synthetic scanner site |
| image_quality_score | Bronze/Silver/Gold | Simulated image quality score |
| prior_condition | Bronze/Silver/Gold | Synthetic clinical comorbidity indicator |
| abnormal_label | Bronze/Silver/Gold | Synthetic binary outcome label |
| is_low_quality_image | Silver/Gold | Derived image quality flag |
| is_cross_sectional | Silver/Gold | Derived CT/MRI flag |
