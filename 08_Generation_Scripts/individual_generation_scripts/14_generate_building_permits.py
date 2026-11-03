"""
14_generate_building_permits.py
Generates Building Permit applications and sanction records:
- 02_Synthetic_Departmental_Records/Building_Permits/building_permits.csv
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

AUTHORITIES = {
    "MH": ["Pune Metropolitan Region Development Authority (PMRDA)", "Nagpur Improvement Trust (NIT)", "Nashik Municipal Town Planning Directorate", "Chhatrapati Sambhajinagar Urban Development Authority", "Kolhapur Town Planning Office"],
    "PB": ["Ludhiana Municipal Corporation Town Planning Branch", "Amritsar Development Authority (ADA)", "Jalandhar Municipal Town Planning Division", "Patiala Urban Planning & Development Authority", "Bathinda Development Authority (BDA)"],
    "GJ": ["Ahmedabad Urban Development Authority (AUDA)", "Surat Urban Development Authority (SUDA)", "Vadodara Urban Development Authority (VUDA)", "Rajkot Urban Development Authority (RUDA)", "Gandhinagar Urban Development Authority (GUDA)"]
}

def generate_building_permits():
    print("[14/20] Generating Synthetic Building Permit Applications & Sanctions...")
    random.seed(config.RANDOM_SEED)
    
    bp_dir = config.DEPT_REC_DIR / "Building_Permits"
    bp_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    # Target parcels that are Residential, Commercial, Industrial, Mixed Use, or Agricultural (farm house)
    eligible = df_parcels[df_parcels["land_use_category"].isin(["Residential", "Commercial", "Industrial", "Mixed Use", "Agricultural"])]
    sampled = eligible.sample(n=min(950, len(eligible)), random_state=config.RANDOM_SEED)
    
    bp_rows = []
    
    for idx, (_, p_row) in enumerate(sampled.iterrows(), start=1):
        p_id = p_row["parcel_id"]
        ulpin = p_row["simulated_ulpin"]
        s_id = p_row["state_id"]
        l_use = p_row["land_use_category"]
        area_m2 = p_row["area_sq_m"]
        
        permit_id = f"BP_{s_id}_{idx:06d}"
        app_year = random.choice([2021, 2022, 2023, 2024])
        app_no = f"BP-APP-{s_id}-{app_year}-{random.randint(1001, 9999)}"
        
        if l_use == "Residential":
            p_type = random.choice(["Individual Residential Villa (G+1)", "Row Housing Scheme", "Residential Apartment Building (G+4)"])
            built_area = round(min(area_m2 * random.uniform(0.4, 0.75), 850.0), 2)
            b_height = round(random.uniform(6.5, 15.0), 2)
        elif l_use == "Commercial":
            p_type = "Commercial Complex & Office Units"
            built_area = round(min(area_m2 * random.uniform(0.6, 1.2), 3500.0), 2)
            b_height = round(random.uniform(12.0, 24.0), 2)
        elif l_use == "Industrial":
            p_type = "Industrial Warehouse & Fabrication Shed"
            built_area = round(min(area_m2 * random.uniform(0.4, 0.65), 5000.0), 2)
            b_height = round(random.uniform(8.0, 14.0), 2)
        elif l_use == "Mixed Use":
            p_type = "Commercial-cum-Residential Building"
            built_area = round(min(area_m2 * random.uniform(0.5, 0.9), 1200.0), 2)
            b_height = round(random.uniform(9.0, 16.0), 2)
        else: # Agricultural
            p_type = "Farmhouse & Allied Agricultural Storage Shed"
            built_area = round(random.uniform(120.0, 300.0), 2)
            b_height = round(random.uniform(4.5, 7.5), 2)
            
        app_date = (datetime.date(app_year, 1, 1) + datetime.timedelta(days=random.randint(1, 280))).isoformat()
        
        app_status = random.choices(["Approved", "Approved", "Approved", "Under_Review", "Rejected"], weights=[75, 10, 5, 6, 4])[0]
        if app_status == "Approved":
            app_dt_obj = datetime.date.fromisoformat(app_date)
            approv_date = (app_dt_obj + datetime.timedelta(days=random.randint(25, 90))).isoformat()
        else:
            approv_date = "N/A"
            
        auth_name = random.choice(AUTHORITIES[s_id])
        
        bp_rows.append({
            "permit_id": permit_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "application_number": app_no,
            "permit_type": p_type,
            "proposed_construction_area_sq_m": built_area,
            "building_height_m": b_height,
            "application_date": app_date,
            "approval_date": approv_date,
            "approval_status": app_status,
            "authority_name": auth_name,
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic municipal / urban development authority building sanction"
        })
        
    df_bp = pd.DataFrame(bp_rows)
    csv_out = bp_dir / "building_permits.csv"
    df_bp.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_bp)} building permit records in {csv_out}")

if __name__ == "__main__":
    generate_building_permits()
