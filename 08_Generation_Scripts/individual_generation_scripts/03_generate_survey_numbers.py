"""
03_generate_survey_numbers.py
Generates realistic synthetic survey-number records linked to parcels.
Outputs:
- 01_Data_Acquisition/Survey_Records/survey_numbers.csv
- 01_Data_Acquisition/Survey_Records/state_survey_config.json
"""

import sys
import os
import json
import random
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_survey_records():
    print("[3/20] Generating Survey Number Records and State Configuration...")
    random.seed(config.RANDOM_SEED)
    
    survey_dir = config.DATA_ACQ_DIR / "Survey_Records"
    survey_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    survey_records = []
    
    for idx, row in df_parcels.iterrows():
        p_id = row["parcel_id"]
        s_id = row["state_id"]
        d_id = row["district_id"]
        v_id = row["village_id"]
        ulpin = row["simulated_ulpin"]
        s_num = row["survey_number"]
        sub_s_num = row["sub_survey_number"]
        
        survey_id = f"SRV_{s_id}_{idx+1:06d}"
        survey_year = random.choice([2018, 2019, 2020, 2021, 2022, 2023])
        
        if s_id == "MH":
            s_type = random.choices(["Cadastral Resurvey (ETS/DGPS)", "Settlement Survey Revision", "Drone Cadastral Survey (SVAMITVA)"], weights=[50, 30, 20])[0]
        elif s_id == "PB":
            s_type = random.choices(["Consolidation Survey (Murabba Bandi)", "Settlement Survey Revision", "Digital Cadastre Ingestion"], weights=[55, 30, 15])[0]
        else: # GJ
            s_type = random.choices(["Re-survey Project (DGPS)", "City Survey Cadastral Mapping", "Revenue Settlement Survey"], weights=[55, 25, 20])[0]
            
        s_status = random.choices(["Settled", "Finalized", "Promulgated", "Under Verification"], weights=[70, 20, 7, 3])[0]
        
        survey_records.append({
            "survey_id": survey_id,
            "survey_number": s_num,
            "sub_survey_number": sub_s_num,
            "full_survey_reference": f"{s_num}/{sub_s_num}",
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "village_id": v_id,
            "district_id": d_id,
            "state_id": s_id,
            "survey_year": survey_year,
            "survey_type": s_type,
            "survey_status": s_status,
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Simulated cadastral survey reference for Land Stack"
        })
        
    df_survey = pd.DataFrame(survey_records)
    csv_out = survey_dir / "survey_numbers.csv"
    df_survey.to_csv(csv_out, index=False)
    
    # Save state survey configuration
    config_out = survey_dir / "state_survey_config.json"
    with open(config_out, "w", encoding="utf-8") as f:
        json.dump(config.SURVEY_CONFIG, f, indent=2)
        
    print(f"  -> Generated {len(df_survey)} survey records in {csv_out}")
    print(f"  -> Saved state survey config in {config_out}")

if __name__ == "__main__":
    generate_survey_records()
