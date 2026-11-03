"""
15_generate_land_restrictions.py
Generates statutory, judicial, and environmental Land Restrictions linked to parcels:
- 02_Synthetic_Departmental_Records/Land_Restrictions/land_restrictions.csv
- 02_Synthetic_Departmental_Records/Land_Restrictions/land_restrictions.geojson
"""

import sys
import os
import json
import random
import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

RESTRICTION_TYPES = [
    {
        "type": "Environmental restriction",
        "desc": "Prohibited non-forest industrial activity within 500m eco-sensitive buffer",
        "auth": "State Environment Impact Assessment Authority (SEIAA)",
        "duration_years": None
    },
    {
        "type": "Government acquisition",
        "desc": "Preliminary notification under Section 11 of Right to Fair Compensation in Land Acquisition Act (RFCTLARR)",
        "auth": "Special Land Acquisition Officer (NHAI Road Widening Cell)",
        "duration_years": 3
    },
    {
        "type": "Court-related restriction",
        "desc": "Interim status-quo injunction in civil title suit #OS-{num}/2022",
        "auth": "Court of Civil Judge Senior Division",
        "duration_years": None
    },
    {
        "type": "Forest restriction",
        "desc": "Boundary buffer notification under Indian Forest Act Section 35 (Soil Conservation Reserve)",
        "auth": "Divisional Forest Officer (Territorial)",
        "duration_years": None
    },
    {
        "type": "Development restriction",
        "desc": "Green Belt reservation in Regional Development Plan 2031 (No construction permitted)",
        "auth": "Metropolitan Region Town Planning Authority",
        "duration_years": None
    },
    {
        "type": "Heritage restriction",
        "desc": "100m prohibited perimeter around protected archaeological monument",
        "auth": "Archaeological Survey of India (Circle Office)",
        "duration_years": None
    }
]

def generate_land_restrictions():
    print("[15/20] Generating Synthetic Land Restrictions (Environmental, Injunctions, Acquisition)...")
    random.seed(config.RANDOM_SEED)
    
    res_dir = config.DEPT_REC_DIR / "Land_Restrictions"
    res_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_geojson_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcels.geojson"
    if not parcels_geojson_path.exists():
        raise FileNotFoundError(f"Missing {parcels_geojson_path}. Run 02_generate_parcels.py first.")
        
    with open(parcels_geojson_path, "r", encoding="utf-8") as f:
        parcels_fc = json.load(f)
        
    # Sample ~450 parcels with restrictions
    total_parcels = len(parcels_fc["features"])
    sample_indices = random.sample(range(total_parcels), 450)
    
    res_rows = []
    res_features = []
    
    for idx, s_idx in enumerate(sample_indices, start=1):
        feat = parcels_fc["features"][s_idx]
        p_props = feat["properties"]
        geom = feat["geometry"]
        
        p_id = p_props["parcel_id"]
        ulpin = p_props["simulated_ulpin"]
        s_id = p_props["state_id"]
        
        res_info = random.choice(RESTRICTION_TYPES)
        res_id = f"RES_{s_id}_{idx:05d}"
        
        start_year = random.choice([2020, 2021, 2022, 2023])
        eff_date = (datetime.date(start_year, 1, 1) + datetime.timedelta(days=random.randint(1, 350))).isoformat()
        
        if res_info["duration_years"]:
            exp_date = (datetime.date(start_year + res_info["duration_years"], 1, 1) + datetime.timedelta(days=random.randint(1, 350))).isoformat()
            status = "Active" if exp_date > "2024-06-01" else "Expired"
        else:
            exp_date = "Indefinite / Subject to Court/Govt Order"
            status = random.choices(["Active", "Active", "Under_Review", "Discharged"], weights=[80, 10, 7, 3])[0]
            
        desc = res_info["desc"].replace("{num}", str(random.randint(101, 899)))
        auth = f"{res_info['auth']}, {p_props['state_name']}"
        
        props = {
            "restriction_id": res_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "state_id": s_id,
            "district_id": p_props["district_id"],
            "village_id": p_props["village_id"],
            "restriction_type": res_info["type"],
            "description": desc,
            "effective_date": eff_date,
            "expiry_date": exp_date,
            "status": status,
            "issuing_authority": auth,
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic statutory / legal restriction register for demonstration"
        }
        
        res_rows.append(props)
        res_features.append({
            "type": "Feature",
            "properties": props,
            "geometry": geom
        })
        
    # Write GeoJSON
    with open(res_dir / "land_restrictions.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": res_features}, f, indent=2)
        
    # Write CSV
    df_res = pd.DataFrame(res_rows)
    df_res.to_csv(res_dir / "land_restrictions.csv", index=False)
    print(f"  -> Generated {len(df_res)} land restrictions in {res_dir}")

if __name__ == "__main__":
    generate_land_restrictions()
