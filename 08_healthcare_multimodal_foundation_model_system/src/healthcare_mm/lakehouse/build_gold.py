def build_gold_patient_encounter_table(sources):
    df = sources["encounters"].merge(sources["patients"], on="patient_id", how="left")
    df = df.merge(sources["labs"], on="encounter_id", how="left")
    df = df.merge(sources["vitals"], on="encounter_id", how="left")
    df = df.merge(sources["notes"], on="encounter_id", how="left")
    df = df.merge(sources["images"], on="encounter_id", how="left")
    return df
