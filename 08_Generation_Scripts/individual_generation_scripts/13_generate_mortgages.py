"""
13_generate_mortgages.py
Generates Mortgage and Encumbrance records for agricultural and commercial parcels:
- 02_Synthetic_Departmental_Records/Mortgages/mortgages_encumbrances.csv
"""

import sys
import os
import random
import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

LENDERS = [
    "State Apex Agriculture & Rural Development Cooperative Bank",
    "National Agro-Refinance Commercial Bank Ltd.",
    "Deccan Farmers Credit Cooperative Society",
    "Punjab Rural Development Banking Corporation",
    "Gujarat Mercantile & Agricultural Credit Society",
    "Central Land Development & Housing Finance Ltd.",
    "Bharat Rural Infrastructure Financial Services"
]

def generate_mortgages():
    print("[13/20] Generating Synthetic Mortgage & Encumbrance Records...")
    random.seed(config.RANDOM_SEED)
    
    mort_dir = config.DEPT_REC_DIR / "Mortgages"
    mort_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    # Select ~1,250 parcels that have had bank loans or mortgages
    sampled = df_parcels.sample(n=1250, random_state=config.RANDOM_SEED)
    
    enc_rows = []
    
    for idx, (_, p_row) in enumerate(sampled.iterrows(), start=1):
        p_id = p_row["parcel_id"]
        ulpin = p_row["simulated_ulpin"]
        s_id = p_row["state_id"]
        l_use = p_row["land_use_category"]
        
        enc_id = f"ENC_{s_id}_{idx:06d}"
        mort_id = f"MTG-{s_id}-{2020 + (idx % 5)}-{random.randint(10000, 99999)}"
        lender = random.choice(LENDERS)
        
        if l_use == "Agricultural":
            loan_amt = round(random.uniform(250000, 1800000), -3) # Kisan Credit Card / Agri term loan
        elif l_use in ["Industrial", "Commercial"]:
            loan_amt = round(random.uniform(2500000, 25000000), -4)
        else:
            loan_amt = round(random.uniform(500000, 4500000), -3)
            
        m_year = random.choice([2019, 2020, 2021, 2022, 2023])
        m_date = (datetime.date(m_year, 1, 1) + datetime.timedelta(days=random.randint(1, 350))).isoformat()
        
        is_released = random.choice([True, False, False]) # ~33% loans released
        if is_released:
            loan_status = "Closed / Discharged"
            enc_status = "Released"
            r_year = min(2024, m_year + random.randint(1, 3))
            rel_date = (datetime.date(r_year, 1, 1) + datetime.timedelta(days=random.randint(1, 350))).isoformat()
        else:
            loan_status = "Active / Servicing"
            enc_status = "Active Encumbrance"
            rel_date = "N/A"
            
        enc_rows.append({
            "encumbrance_id": enc_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "mortgage_id": mort_id,
            "lender_name": lender,
            "loan_amount_inr": loan_amt,
            "mortgage_date": m_date,
            "loan_status": loan_status,
            "release_date": rel_date,
            "encumbrance_status": enc_status,
            "charge_type": "First Registered Equitable Mortgage",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic banking encumbrance register"
        })
        
    df_enc = pd.DataFrame(enc_rows)
    csv_out = mort_dir / "mortgages_encumbrances.csv"
    df_enc.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_enc)} mortgage and encumbrance records in {csv_out}")

if __name__ == "__main__":
    generate_mortgages()
