"""
08_generate_utilities.py
Generates synthetic utility infrastructure (Power lines, Poles, Water mains, Drainage, Telecom):
- 01_Data_Acquisition/Utilities/utilities.geojson
- 01_Data_Acquisition/Utilities/utilities.csv
"""

import sys
import os
import json
import random
from pathlib import Path
import pandas as pd
from shapely.geometry import Point, LineString, mapping

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_utilities():
    print("[8/20] Generating Synthetic Utility Infrastructure (Power, Water, Drainage, Telecom)...")
    random.seed(config.RANDOM_SEED)
    
    util_dir = config.DATA_ACQ_DIR / "Utilities"
    util_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    util_features = []
    util_rows = []
    util_counter = 1
    
    # Group parcels by village
    village_groups = df_parcels.groupby("village_id")
    
    for vil_id, group in village_groups:
        row0 = group.iloc[0]
        s_id = row0["state_id"]
        d_id = row0["district_id"]
        vil_name = row0["village_name"]
        
        # Centroid of the village cluster
        mean_lat = group["centroid_latitude"].mean()
        mean_lon = group["centroid_longitude"].mean()
        
        # 1. 11kV Electricity Feeder Line (LineString)
        line_id = f"UTL_{s_id}_{util_counter:06d}"
        util_counter += 1
        p_line = LineString([
            (mean_lon - 0.009, mean_lat - 0.007),
            (mean_lon - 0.002, mean_lat - 0.001),
            (mean_lon + 0.004, mean_lat + 0.003),
            (mean_lon + 0.008, mean_lat + 0.007)
        ])
        p_line_props = {
            "utility_id": line_id,
            "utility_type": "Electricity Distribution Line (11kV)",
            "parcel_id": "MULTIPLE_PARCEL_RIGHT_OF_WAY",
            "simulated_ulpin": "CORRIDOR_OVERLAY",
            "village_id": vil_id,
            "village_name": vil_name,
            "district_id": d_id,
            "state_id": s_id,
            "installation_year": random.choice([2012, 2015, 2018, 2020]),
            "operational_status": "Operational",
            "capacity_spec": "11 kV High Tension 3-Phase Overhead Cable",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic utility transmission corridor"
        }
        util_rows.append(p_line_props)
        util_features.append({"type": "Feature", "properties": p_line_props, "geometry": mapping(p_line)})
        
        # 2. Potable Water Supply Pipeline (LineString)
        w_id = f"UTL_{s_id}_{util_counter:06d}"
        util_counter += 1
        w_line = LineString([
            (mean_lon - 0.007, mean_lat + 0.006),
            (mean_lon, mean_lat),
            (mean_lon + 0.006, mean_lat - 0.005)
        ])
        w_props = {
            "utility_id": w_id,
            "utility_type": "Water Supply Pipeline",
            "parcel_id": "PUBLIC_ROAD_RIGHT_OF_WAY",
            "simulated_ulpin": "UTILITY_CORRIDOR",
            "village_id": vil_id,
            "village_name": vil_name,
            "district_id": d_id,
            "state_id": s_id,
            "installation_year": random.choice([2016, 2019, 2021, 2023]),
            "operational_status": "Operational",
            "capacity_spec": "200mm DI Potable Main Distribution",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic rural water pipeline network"
        }
        util_rows.append(w_props)
        util_features.append({"type": "Feature", "properties": w_props, "geometry": mapping(w_line)})
        
        # 3. Underground Drainage Main Line (LineString)
        d_id_code = f"UTL_{s_id}_{util_counter:06d}"
        util_counter += 1
        d_line = LineString([
            (mean_lon - 0.004, mean_lat - 0.004),
            (mean_lon, mean_lat),
            (mean_lon + 0.005, mean_lat + 0.002)
        ])
        d_props = {
            "utility_id": d_id_code,
            "utility_type": "Drainage Pipeline",
            "parcel_id": "ROAD_MARGIN_RESERVE",
            "simulated_ulpin": "DRAINAGE_NETWORK",
            "village_id": vil_id,
            "village_name": vil_name,
            "district_id": d_id,
            "state_id": s_id,
            "installation_year": random.choice([2017, 2020, 2022]),
            "operational_status": "Operational",
            "capacity_spec": "450mm RCC Gravity Storm/Sullage Drain",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic drainage line"
        }
        util_rows.append(d_props)
        util_features.append({"type": "Feature", "properties": d_props, "geometry": mapping(d_line)})
        
        # 4. Telecom Tower (Point) linked to 1 specific commercial / vacant parcel
        tower_parcel = group[group["land_use_category"].isin(["Commercial", "Vacant Land", "Industrial"])].iloc[0] if len(group[group["land_use_category"].isin(["Commercial", "Vacant Land", "Industrial"])]) > 0 else group.iloc[5]
        tel_id = f"UTL_{s_id}_{util_counter:06d}"
        util_counter += 1
        tel_pt = Point(tower_parcel["centroid_longitude"] + 0.0001, tower_parcel["centroid_latitude"] + 0.0001)
        tel_props = {
            "utility_id": tel_id,
            "utility_type": "Telecom Infrastructure",
            "parcel_id": tower_parcel["parcel_id"],
            "simulated_ulpin": tower_parcel["simulated_ulpin"],
            "village_id": vil_id,
            "village_name": vil_name,
            "district_id": d_id,
            "state_id": s_id,
            "installation_year": 2021,
            "operational_status": "Operational",
            "capacity_spec": "40m Ground-Based Telecom Tower (4G/5G Shared RAN)",
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic telecommunication mast asset"
        }
        util_rows.append(tel_props)
        util_features.append({"type": "Feature", "properties": tel_props, "geometry": mapping(tel_pt)})
        
        # 5. Electricity Distribution Transformers & Poles (Points) on 6 specific parcels
        sample_parcels = group.sample(min(8, len(group)), random_state=config.RANDOM_SEED)
        for _, p_row in sample_parcels.iterrows():
            pole_id = f"UTL_{s_id}_{util_counter:06d}"
            util_counter += 1
            pole_pt = Point(p_row["centroid_longitude"], p_row["centroid_latitude"])
            pole_props = {
                "utility_id": pole_id,
                "utility_type": "Electricity Pole / Transformer",
                "parcel_id": p_row["parcel_id"],
                "simulated_ulpin": p_row["simulated_ulpin"],
                "village_id": vil_id,
                "village_name": vil_name,
                "district_id": d_id,
                "state_id": s_id,
                "installation_year": random.choice([2015, 2018, 2021]),
                "operational_status": "Operational",
                "capacity_spec": "100 kVA Distribution Transformer Substation",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic local distribution asset"
            }
            util_rows.append(pole_props)
            util_features.append({"type": "Feature", "properties": pole_props, "geometry": mapping(pole_pt)})
            
    # Write GeoJSON
    with open(util_dir / "utilities.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": util_features}, f, indent=2)
        
    # Write CSV
    pd.DataFrame(util_rows).to_csv(util_dir / "utilities.csv", index=False)
    print(f"  -> Generated {len(util_rows)} utility features in {util_dir}")

if __name__ == "__main__":
    generate_utilities()
