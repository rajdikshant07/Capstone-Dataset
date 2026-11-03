"""
09_generate_ownership.py
Generates realistic synthetic land ownership records:
- 02_Synthetic_Departmental_Records/Ownership/ownership_records.csv
Supports Individual, Joint, Company, Government, and Trust ownership with fractional shares.
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

NAME_POOLS = {
    "MH": {
        "first": ["Ramesh", "Suresh", "Sunil", "Vilas", "Ganesh", "Prakash", "Sanjay", "Sachin", "Deepak", "Nitin", "Anjali", "Sunita", "Vandana", "Savita", "Rekha", "Pradeep", "Mahesh", "Ashok"],
        "last": ["Deshmukh", "Patil", "Kulkarni", "Shinde", "Pawar", "Gaikwad", "Jadhav", "More", "Joshi", "Chavan", "Bhosale", "Salunke", "Kadam", "Thorat"],
        "fictional_addr": "Plot {num}, Near Shivaji Chowk, {vil}, {dist}, Maharashtra - 411001"
    },
    "PB": {
        "first": ["Harpreet", "Gurpreet", "Jaswinder", "Kuldeep", "Balwinder", "Manpreet", "Sukhwinder", "Rajinder", "Amandeep", "Paramjit", "Harjit", "Simranjit", "Tarlochan", "Satnam"],
        "last": ["Singh", "Kaur", "Dhillon", "Sandhu", "Grewal", "Gill", "Brar", "Sidhu", "Bajwa", "Cheema", "Mann", "Virk", "Chahal"],
        "fictional_addr": "Kothi No. {num}, GT Road Enclave, {vil}, {dist}, Punjab - 141001"
    },
    "GJ": {
        "first": ["Rajesh", "Bharat", "Jayesh", "Hitesh", "Mukesh", "Paresh", "Naresh", "Alpesh", "Bhavin", "Manish", "Neetaben", "Gitaben", "Hetalben", "Hansaben", "Kirit", "Dharmesh"],
        "last": ["Patel", "Shah", "Mehta", "Desai", "Joshi", "Trivedi", "Vora", "Solanki", "Prajapati", "Pandya", "Bhatt", "Parmar", "Gadhvi"],
        "fictional_addr": "Bunglow No. {num}, Sardar Patel Society, {vil}, {dist}, Gujarat - 380001"
    }
}

COMPANIES = [
    "Kisan Agro Farms Pvt Ltd", "Deccan Logistics Infrastructure Ltd", "Shivalik Green Energy Ltd",
    "Sardar Agro Processing LLP", "Western Industrial Warehousing Corp", "Greenfield Bio-Agri Projects Ltd"
]

GOVT_ENTITIES = {
    "MH": "Revenue & Forest Department, Government of Maharashtra",
    "PB": "Department of Agriculture & Farmers Welfare, Punjab",
    "GJ": "Gujarat Industrial Development Corporation (GIDC)"
}

TRUSTS = [
    "Shree Siddhivinayak Gramin Vikas Trust", "Guru Nanak Dev Charitable Educational Trust",
    "Sardar Vallabhbhai Rural Welfare Foundation", "Swaminarayan Seva & Agriculture Trust"
]

def generate_ownership():
    print("[9/20] Generating Synthetic Parcel Ownership Records (Individual, Joint, Corporate, Trust)...")
    random.seed(config.RANDOM_SEED)
    
    own_dir = config.DEPT_REC_DIR / "Ownership"
    own_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    ownership_rows = []
    owner_counter = 1
    
    for _, row in df_parcels.iterrows():
        p_id = row["parcel_id"]
        ulpin = row["simulated_ulpin"]
        s_id = row["state_id"]
        s_name = row["state_name"]
        d_id = row["district_id"]
        d_name = row["district_name"]
        v_id = row["village_id"]
        v_name = row["village_name"]
        l_use = row["land_use_category"]
        
        # Determine ownership structure
        if l_use == "Government":
            own_type = "Government"
            owner_name = GOVT_ENTITIES.get(s_id, f"State Government of {s_name}")
            addr = f"Administrative Complex, {d_name} Collectorate, {s_name}"
            owner_id = f"OWN_{s_id}_{owner_counter:06d}"
            owner_counter += 1
            acq_date = "1975-04-01"
            ownership_rows.append({
                "owner_id": owner_id,
                "parcel_id": p_id,
                "simulated_ulpin": ulpin,
                "owner_name": owner_name,
                "ownership_type": own_type,
                "ownership_percentage": 100.0,
                "fictional_address": addr,
                "state_id": s_id,
                "district_id": d_id,
                "village_id": v_id,
                "acquisition_date": acq_date,
                "ownership_status": "Active",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic government parcel title record"
            })
            continue
            
        elif l_use == "Industrial" and random.random() < 0.60:
            own_type = "Company"
            owner_name = random.choice(COMPANIES)
            addr = f"Registered Corporate Office, Phase-II Industrial Estate, {d_name}"
            owner_id = f"OWN_{s_id}_{owner_counter:06d}"
            owner_counter += 1
            acq_date = (datetime.date(2015, 1, 1) + datetime.timedelta(days=random.randint(0, 2500))).isoformat()
            ownership_rows.append({
                "owner_id": owner_id,
                "parcel_id": p_id,
                "simulated_ulpin": ulpin,
                "owner_name": owner_name,
                "ownership_type": own_type,
                "ownership_percentage": 100.0,
                "fictional_address": addr,
                "state_id": s_id,
                "district_id": d_id,
                "village_id": v_id,
                "acquisition_date": acq_date,
                "ownership_status": "Active",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic corporate ownership record"
            })
            continue
            
        elif random.random() < 0.03: # Trust
            own_type = "Trust"
            owner_name = random.choice(TRUSTS)
            addr = f"Trust Bhavan, Post Box 14, {v_name}, {d_name}"
            owner_id = f"OWN_{s_id}_{owner_counter:06d}"
            owner_counter += 1
            acq_date = "1998-08-15"
            ownership_rows.append({
                "owner_id": owner_id,
                "parcel_id": p_id,
                "simulated_ulpin": ulpin,
                "owner_name": owner_name,
                "ownership_type": own_type,
                "ownership_percentage": 100.0,
                "fictional_address": addr,
                "state_id": s_id,
                "district_id": d_id,
                "village_id": v_id,
                "acquisition_date": acq_date,
                "ownership_status": "Active",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic charitable trust ownership record"
            })
            continue
            
        # Individual or Joint ownership
        is_joint = random.random() < 0.28 # ~28% joint ownership
        pool = NAME_POOLS[s_id]
        
        if not is_joint:
            # Single individual owner
            fn = random.choice(pool["first"])
            ln = random.choice(pool["last"])
            full_name = f"{fn} {ln}"
            addr = pool["fictional_addr"].format(num=random.randint(10, 499), vil=v_name, dist=d_name)
            owner_id = f"OWN_{s_id}_{owner_counter:06d}"
            owner_counter += 1
            acq_date = (datetime.date(2005, 1, 1) + datetime.timedelta(days=random.randint(0, 6000))).isoformat()
            
            ownership_rows.append({
                "owner_id": owner_id,
                "parcel_id": p_id,
                "simulated_ulpin": ulpin,
                "owner_name": full_name,
                "ownership_type": "Individual",
                "ownership_percentage": 100.0,
                "fictional_address": addr,
                "state_id": s_id,
                "district_id": d_id,
                "village_id": v_id,
                "acquisition_date": acq_date,
                "ownership_status": "Active",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic individual private land title record"
            })
        else:
            # Joint ownership (2 or 3 co-owners, e.g. siblings or spouses)
            co_owner_count = 2 if random.random() < 0.85 else 3
            common_ln = random.choice(pool["last"])
            
            if co_owner_count == 2:
                shares = [50.0, 50.0] if random.random() < 0.70 else [60.0, 40.0]
            else:
                shares = [33.34, 33.33, 33.33]
                
            acq_date = (datetime.date(2008, 1, 1) + datetime.timedelta(days=random.randint(0, 5000))).isoformat()
            
            for s_pct in shares:
                fn = random.choice(pool["first"])
                full_name = f"{fn} {common_ln}"
                addr = pool["fictional_addr"].format(num=random.randint(10, 499), vil=v_name, dist=d_name)
                owner_id = f"OWN_{s_id}_{owner_counter:06d}"
                owner_counter += 1
                
                ownership_rows.append({
                    "owner_id": owner_id,
                    "parcel_id": p_id,
                    "simulated_ulpin": ulpin,
                    "owner_name": full_name,
                    "ownership_type": "Joint",
                    "ownership_percentage": s_pct,
                    "fictional_address": addr,
                    "state_id": s_id,
                    "district_id": d_id,
                    "village_id": v_id,
                    "acquisition_date": acq_date,
                    "ownership_status": "Active",
                    "data_status": config.DATA_STATUS["SYNTHETIC"],
                    "provenance": "Synthetic joint co-ownership fractional title"
                })
                
    df_own = pd.DataFrame(ownership_rows)
    csv_out = own_dir / "ownership_records.csv"
    df_own.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_own)} ownership records for {len(df_parcels)} parcels in {csv_out}")
    return df_own

if __name__ == "__main__":
    generate_ownership()
