"""
10_generate_ror.py
Generates Record of Rights (RoR) records simulating state-specific revenue extracts:
- Maharashtra: 7/12 Extract (Saat-Baara)
- Punjab: Jamabandi Nakal
- Gujarat: Village Form 7/12 (VF-7/12)
Outputs:
- 02_Synthetic_Departmental_Records/RoR/ror_records.csv
"""

import sys
import os
import random
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

CROPS_BY_STATE = {
    "MH": ["Sugarcane (Adsali)", "Cotton (Bt Hybrid)", "Soybean (JS 335)", "Onion (Rabi)", "Pomegranate", "Grapes", "Jowar", "Gram / Chana"],
    "PB": ["Wheat (HD-2967)", "Paddy (PR-126)", "Basmati Rice (Pusa 1121)", "Mustard / Sarson", "Maize", "Fodder / Barseem"],
    "GJ": ["Groundnut (GG-20)", "Cotton (Shankar-6)", "Castor (GCH-7)", "Cumin / Jeera", "Wheat (GW-496)", "Tobacco", "Fodder / Jowar"]
}

def generate_ror():
    print("[10/20] Generating Synthetic Record of Rights (RoR / 7-12 / Jamabandi) Dataset...")
    random.seed(config.RANDOM_SEED)
    
    ror_dir = config.DEPT_REC_DIR / "RoR"
    ror_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    ownership_path = config.DEPT_REC_DIR / "Ownership" / "ownership_records.csv"
    
    if not parcels_attr_path.exists() or not ownership_path.exists():
        raise FileNotFoundError("Missing prerequisite files. Ensure parcels and ownership scripts have executed.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    df_own = pd.read_csv(ownership_path)
    
    # Get primary owner for each parcel
    primary_owners = df_own.drop_duplicates(subset=["parcel_id"], keep="first").set_index("parcel_id")
    
    ror_rows = []
    
    for idx, p_row in df_parcels.iterrows():
        p_id = p_row["parcel_id"]
        ulpin = p_row["simulated_ulpin"]
        s_id = p_row["state_id"]
        s_num = p_row["survey_number"]
        sub_s_num = p_row["sub_survey_number"]
        l_use = p_row["land_use_category"]
        area_ha = p_row["area_hectares"]
        
        # Owner ID
        owner_id = primary_owners.loc[p_id]["owner_id"] if p_id in primary_owners.index else f"OWN_{s_id}_000001"
        khata_no = random.randint(101, 899)
        
        ror_id = f"ROR_{s_id}_{idx+1:06d}"
        
        if s_id == "MH":
            doc_type = "7/12 Extract (Saat-Baara)"
            tenure = random.choice(["Occupant Class I (Bhogavatdar Varg-1)", "Occupant Class II (Bhogavatdar Varg-2)", "Government Lessee"])
            if l_use == "Agricultural":
                cult_crop = random.choice(CROPS_BY_STATE["MH"])
                irrig = random.choice(["Well / Borewell (Vihir/Kupnalika)", "Canal Irrigated (Patbandhare)", "Rainfed (Jirayat)"])
                land_cls = "Jirayat (Dry Crop)" if irrig == "Rainfed (Jirayat)" else "Bagayat (Garden/Irrigated)"
            else:
                cult_crop = "Non-Cultivable / Non-Agricultural (NA)"
                irrig = "Municipal / Commercial Connection"
                land_cls = "Non-Agricultural (Akarani Form 8A)"
                
            state_specific_meta = f"Khata No: {khata_no}, Pot-Kharaba: 0.02 Ha, Mutation Entry (Ferfar): #{random.randint(1200, 9999)}"
            
        elif s_id == "PB":
            doc_type = "Jamabandi Nakal (Record of Rights)"
            tenure = random.choice(["Owner / Maroosi (Ala Malik)", "Occupancy Tenant (Muzaria)", "Pattadar / Leaseholder"])
            if l_use == "Agricultural":
                cult_crop = random.choice(CROPS_BY_STATE["PB"])
                irrig = random.choice(["Tubewell (Nalka)", "Canal (Nehri)", "Rainfed (Barani)"])
                land_cls = "Chahi (Well/Tubewell Irrigated)" if "Tubewell" in irrig else ("Nehri (Canal)" if "Canal" in irrig else "Barani (Rainfed)")
            else:
                cult_crop = "Gair Mumkin (Unculturable / Built-up)"
                irrig = "Commercial / Civil Supply"
                land_cls = "Gair Mumkin Abadi / Karkhana"
                
            khewat = random.randint(50, 400)
            khatoni = random.randint(100, 700)
            state_specific_meta = f"Khewat No: {khewat}, Khatoni No: {khatoni}, Land Revenue: Rs. {random.randint(25, 250)}"
            
        else: # GJ
            doc_type = "Village Form 7/12 (VF-7/12 Hakk Patra)"
            tenure = random.choice(["Old Tenure (Juni Sharat)", "New Tenure (Navi Sharat)", "Restricted Agricultural Tenure"])
            if l_use == "Agricultural":
                cult_crop = random.choice(CROPS_BY_STATE["GJ"])
                irrig = random.choice(["Borewell / Submersible", "Narmada Canal Lift", "Rainfed / Monsoon"])
                land_cls = "Kyari (Paddy Field)" if "Canal" in irrig else ("Bagayat" if "Borewell" in irrig else "Jirayat")
            else:
                cult_crop = "Bin Kheti (Non-Agricultural Industrial/Residential)"
                irrig = "Local Authority Water Main"
                land_cls = "Bin Kheti (NA Order Approved)"
                
            state_specific_meta = f"Khata No: {khata_no}, Entry No (Kachhi-Pakkhi Nondh): #{random.randint(2000, 8500)}"
            
        ror_rows.append({
            "ror_id": ror_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "survey_number": s_num,
            "sub_survey_number": sub_s_num,
            "primary_owner_id": owner_id,
            "land_classification": land_cls,
            "cultivation_details": cult_crop,
            "irrigation_status": irrig,
            "tenure_type": tenure,
            "state_ror_extract_type": doc_type,
            "state_specific_metadata": state_specific_meta,
            "record_year": 2024,
            "record_status": "Certified",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic computerized land record extract for Land Stack"
        })
        
    df_ror = pd.DataFrame(ror_rows)
    csv_out = ror_dir / "ror_records.csv"
    df_ror.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_ror)} RoR extract records in {csv_out}")

if __name__ == "__main__":
    generate_ror()
