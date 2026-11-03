"""
05_generate_land_use.py
Generates Land Use and Land Cover (LULC) dataset:
- 01_Data_Acquisition/Land_Use/land_use.geojson
- 01_Data_Acquisition/Land_Use/land_use.csv
- 01_Data_Acquisition/Land_Use/land_use_metadata.json
"""

import sys
import os
import json
import random
from pathlib import Path
import pandas as pd
from shapely.geometry import shape, mapping

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

LULC_MAP = {
    "Agricultural": [
        ("Cropland Irrigated", "Cropland"),
        ("Cropland Rainfed", "Cropland"),
        ("Plantation (Horticulture/Orchards)", "Plantation"),
        ("Fallow Land (Current Fallow)", "Fallow Land")
    ],
    "Residential": [
        ("Built-up Rural Settlement (Abadi)", "Built-up Area"),
        ("Built-up Peri-Urban Plotted Development", "Built-up Area")
    ],
    "Commercial": [
        ("Commercial Retail & Market Yard", "Built-up Area")
    ],
    "Industrial": [
        ("Agro-Processing & Industrial Unit", "Built-up Area")
    ],
    "Government": [
        ("Public Institutional & Administrative", "Built-up Area")
    ],
    "Forest": [
        ("Protected Forest & Deciduous Scrub", "Forest"),
        ("Grassland & Grazing Land (Gauchar)", "Grassland")
    ],
    "Mixed Use": [
        ("Mixed Commercial-Residential Area", "Built-up Area")
    ],
    "Vacant Land": [
        ("Barren & Uncultivable Land", "Barren Land"),
        ("Open Scrub & Grazing Commons", "Grassland")
    ]
}

def generate_land_use():
    print("[5/20] Generating Land Use and Land Cover (LULC) Dataset...")
    random.seed(config.RANDOM_SEED)
    
    lu_dir = config.DATA_ACQ_DIR / "Land_Use"
    lu_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_geojson_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcels.geojson"
    if not parcels_geojson_path.exists():
        raise FileNotFoundError(f"Missing {parcels_geojson_path}. Run 02_generate_parcels.py first.")
        
    with open(parcels_geojson_path, "r", encoding="utf-8") as f:
        parcels_fc = json.load(f)
        
    lu_features = []
    lu_rows = []
    
    for idx, feat in enumerate(parcels_fc["features"], start=1):
        p_props = feat["properties"]
        geom = feat["geometry"]
        p_cat = p_props["land_use_category"]
        
        # Select subcategory and standardized LULC class
        options = LULC_MAP.get(p_cat, [("Cropland Irrigated", "Cropland")])
        subcat, lulc_class = random.choice(options)
        
        lu_id = f"LU_{p_props['state_id']}_{idx:06d}"
        class_year = 2024
        source = "Simulated Multi-Spectral Optical Satellite Classification (Sentinel-2 10m L2A Simulation)"
        conf_score = round(random.uniform(0.86, 0.98), 3)
        
        props = {
            "land_use_id": lu_id,
            "parcel_id": p_props["parcel_id"],
            "simulated_ulpin": p_props["simulated_ulpin"],
            "state_id": p_props["state_id"],
            "state_name": p_props["state_name"],
            "district_id": p_props["district_id"],
            "district_name": p_props["district_name"],
            "village_id": p_props["village_id"],
            "village_name": p_props["village_name"],
            "land_use_category": lulc_class,
            "land_use_subcategory": subcat,
            "parcel_category": p_cat,
            "classification_year": class_year,
            "classification_source": source,
            "confidence_score": conf_score,
            "area_sq_m": p_props["area_sq_m"],
            "area_hectares": p_props["area_hectares"],
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Simulated raster-to-cadastral zonal aggregation for Land Stack Module 1"
        }
        
        lu_rows.append(props)
        lu_features.append({
            "type": "Feature",
            "properties": props,
            "geometry": geom
        })
        
    # Write GeoJSON
    with open(lu_dir / "land_use.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": lu_features}, f)
        
    # Write CSV
    df_lu = pd.DataFrame(lu_rows)
    df_lu.to_csv(lu_dir / "land_use.csv", index=False)
    
    # Write Metadata JSON
    metadata = {
        "dataset_name": "Land Stack Simulated Land Use & Land Cover (LULC)",
        "version": "1.0.0",
        "spatial_coverage": ["Maharashtra", "Punjab", "Gujarat"],
        "crs": config.CRS_NAME,
        "total_records": len(lu_rows),
        "classes_represented": list(df_lu["land_use_category"].unique()),
        "classification_method": "Simulated Random Forest Cadastral Zonal Aggregation",
        "raster_simulation_spec": {
            "nominal_ground_resolution": "10 meters",
            "spectral_bands": ["Blue", "Green", "Red", "NIR", "SWIR-1", "SWIR-2"],
            "indices": ["NDVI", "NDWI", "NDBI"],
            "synthetic_disclaimer": "Simulated vector classification layer. Not derived from actual proprietary commercial satellite imagery."
        },
        "accuracy_metrics": {
            "simulated_mean_confidence": round(df_lu["confidence_score"].mean(), 4),
            "simulated_overall_accuracy": "91.4%"
        },
        "data_status": "SYNTHETIC"
    }
    with open(lu_dir / "land_use_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"  -> Generated {len(lu_rows)} LULC features in {lu_dir / 'land_use.geojson'}")
    print(f"  -> Generated CSV and metadata in {lu_dir}")

if __name__ == "__main__":
    generate_land_use()
