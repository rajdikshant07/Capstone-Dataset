"""
11_generate_registration.py
Generates Property Registration deed transaction records:
- 02_Synthetic_Departmental_Records/Registration/property_registration.csv
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

SRO_OFFICES = {
    "MH": ["SRO Haveli No. 3 (Pune)", "SRO Nagpur Rural", "SRO Nashik Central", "SRO Sambhajinagar Cantonment", "SRO Karveer (Kolhapur)"],
    "PB": ["SRO Amritsar North", "SRO Ludhiana Central", "SRO Jalandhar West", "SRO Patiala Sadar", "SRO Bathinda City"],
    "GJ": ["SRO Ahmedabad-12 (Sanand)", "SRO Surat South (Majura)", "SRO Vadodara Central", "SRO Rajkot City", "SRO Gandhinagar Sub-District"]
}

def generate_registration():
    print("[11/20] Generating Synthetic Property Registration Deeds (Sale, Gift, Inheritance, Lease, Partition)...")
    random.seed(config.RANDOM_SEED)
    
    reg_dir = config.DEPT_REC_DIR / "Registration"
    reg_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    ownership_path = config.DEPT_REC_DIR / "Ownership" / "ownership_records.csv"
    
    if not parcels_attr_path.exists() or not ownership_path.exists():
        raise FileNotFoundError("Missing prerequisite files. Ensure parcels and ownership scripts have executed.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    df_own = pd.read_csv(ownership_path)
    owner_ids = df_own["owner_id"].tolist()
    
    # Select ~2,500 parcels that have recorded registration history
    sampled_parcels = df_parcels.sample(n=2500, random_state=config.RANDOM_SEED)
    
    reg_rows = []
    
    for idx, (_, p_row) in enumerate(sampled_parcels.iterrows(), start=1):
        p_id = p_row["parcel_id"]
        ulpin = p_row["simulated_ulpin"]
        s_id = p_row["state_id"]
        d_name = p_row["district_name"]
        l_use = p_row["land_use_category"]
        area_m2 = p_row["area_sq_m"]
        
        reg_id = f"REG_{s_id}_{idx:06d}"
        
        deed_type = random.choices(
            ["Sale Deed", "Gift Deed", "Inheritance / Succession", "Lease Deed (30 Yrs)", "Partition Deed", "Mortgage Deed"],
            weights=[50, 15, 15, 8, 7, 5], k=1
        )[0]
        
        # Transaction value based on land use and area
        if l_use in ["Commercial", "Mixed Use"]:
            rate_per_sqm = random.uniform(25000, 75000)
        elif l_use == "Residential":
            rate_per_sqm = random.uniform(8000, 28000)
        elif l_use == "Industrial":
            rate_per_sqm = random.uniform(4000, 12000)
        else: # Agricultural, Forest, Vacant
            rate_per_sqm = random.uniform(150, 800)
            
        trans_val = round(area_m2 * rate_per_sqm, -3) # Round to nearest 1000
        trans_val = max(150000.0, min(trans_val, 85000000.0))
        
        # Stamp duty (~5-7%) and Reg Fee (~1%)
        stamp_rate = 0.06 if s_id == "MH" else (0.05 if s_id == "GJ" else 0.07)
        stamp_duty = round(trans_val * stamp_rate, 2)
        reg_fee = round(min(trans_val * 0.01, 30000.0), 2)
        
        # Seller and Buyer
        seller_id = random.choice(owner_ids)
        buyer_id = random.choice(owner_ids)
        while buyer_id == seller_id:
            buyer_id = random.choice(owner_ids)
            
        reg_year = random.choice([2019, 2020, 2021, 2022, 2023, 2024])
        reg_date = (datetime.date(reg_year, 1, 1) + datetime.timedelta(days=random.randint(1, 350))).isoformat()
        deed_no = f"DOC-{s_id}-{reg_year}-{random.randint(1001, 9999)}"
        
        sro_name = random.choice(SRO_OFFICES[s_id])
        reg_status = random.choices(["Registered", "Registered", "Registered", "Scanned_and_Archived"], weights=[70, 15, 10, 5])[0]
        
        reg_rows.append({
            "registration_id": reg_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "deed_number": deed_no,
            "deed_type": deed_type,
            "seller_owner_id": seller_id,
            "buyer_owner_id": buyer_id,
            "registration_date": reg_date,
            "transaction_value_inr": trans_val,
            "stamp_duty_inr": stamp_duty,
            "registration_fee_inr": reg_fee,
            "sub_registrar_office": sro_name,
            "registration_status": reg_status,
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic computerized property registration deed transaction"
        })
        
    df_reg = pd.DataFrame(reg_rows)
    csv_out = reg_dir / "property_registration.csv"
    df_reg.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_reg)} property registration deeds in {csv_out}")

if __name__ == "__main__":
    generate_registration()
