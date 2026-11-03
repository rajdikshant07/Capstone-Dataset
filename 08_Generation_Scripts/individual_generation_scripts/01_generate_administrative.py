"""
01_generate_administrative.py
Generates administrative geography layers:
- states.geojson & states.csv
- districts.geojson & districts.csv
- villages.geojson & villages.csv
"""

import sys
import os
import json
from pathlib import Path
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon, box, mapping

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_administrative_layers():
    print("[1/20] Generating Administrative Geography Layers (States, Districts, Villages)...")
    
    admin_dir = config.DATA_ACQ_DIR / "Administrative_Geography"
    admin_dir.mkdir(parents=True, exist_ok=True)
    
    states_features = []
    districts_features = []
    villages_features = []
    
    states_rows = []
    districts_rows = []
    villages_rows = []
    
    for state_id, state_info in config.ADMIN_HIERARCHY.items():
        state_districts = state_info["districts"]
        state_lat = state_info["ref_coords"]["lat"]
        state_lon = state_info["ref_coords"]["lon"]
        
        district_boxes = []
        
        for dist_id, dist_info in state_districts.items():
            dist_lat = dist_info["lat"]
            dist_lon = dist_info["lon"]
            
            # Synthetic bounding polygon for district (approx 0.45 deg box around HQ with slight perturbation)
            dist_poly = box(dist_lon - 0.25, dist_lat - 0.22, dist_lon + 0.25, dist_lat + 0.22)
            district_boxes.append(dist_poly)
            
            dist_props = {
                "district_id": dist_id,
                "district_code": dist_info["district_code"],
                "district_name": dist_info["district_name"],
                "state_id": state_id,
                "state_name": state_info["state_name"],
                "headquarters": dist_info["headquarters"],
                "latitude": dist_lat,
                "longitude": dist_lon,
                "sample_village_count": len(dist_info["villages"]),
                "boundary_type": "SYNTHETIC_ENVELOPE",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Generated synthetic district anchor for Land Stack simulation"
            }
            districts_rows.append(dist_props)
            districts_features.append({
                "type": "Feature",
                "properties": dist_props,
                "geometry": mapping(dist_poly)
            })
            
            # Villages in this district
            for v_info in dist_info["villages"]:
                v_lat = round(dist_lat + v_info["lat_offset"], 6)
                v_lon = round(dist_lon + v_info["lon_offset"], 6)
                
                # Synthetic village boundary polygon (approx 0.035 deg box ~3.5 km across)
                v_poly = box(v_lon - 0.018, v_lat - 0.016, v_lon + 0.018, v_lat + 0.016)
                
                v_props = {
                    "village_id": v_info["village_id"],
                    "village_code": v_info["village_code"],
                    "village_name": v_info["village_name"],
                    "district_id": dist_id,
                    "district_name": dist_info["district_name"],
                    "state_id": state_id,
                    "state_name": state_info["state_name"],
                    "village_type": v_info["village_type"],
                    "population_category": v_info["population_cat"],
                    "target_parcel_count": config.TARGET_PARCELS_PER_VILLAGE,
                    "centroid_latitude": v_lat,
                    "centroid_longitude": v_lon,
                    "boundary_type": "SYNTHETIC_CADASTRAL_ZONE",
                    "data_status": config.DATA_STATUS["SYNTHETIC"],
                    "provenance": "Generated synthetic village zone for Land Stack demonstration"
                }
                villages_rows.append(v_props)
                villages_features.append({
                    "type": "Feature",
                    "properties": v_props,
                    "geometry": mapping(v_poly)
                })
        
        # State boundary: Convex hull of district bounding boxes or bounding box
        state_min_lon = min(d.bounds[0] for d in district_boxes) - 0.2
        state_min_lat = min(d.bounds[1] for d in district_boxes) - 0.2
        state_max_lon = max(d.bounds[2] for d in district_boxes) + 0.2
        state_max_lat = max(d.bounds[3] for d in district_boxes) + 0.2
        state_poly = box(state_min_lon, state_min_lat, state_max_lon, state_max_lat)
        
        state_props = {
            "state_id": state_id,
            "state_code": state_info["state_code"],
            "state_name": state_info["state_name"],
            "state_abbr": state_info["state_abbr"],
            "ref_latitude": state_lat,
            "ref_longitude": state_lon,
            "sample_district_count": len(state_districts),
            "sample_village_count": sum(len(d["villages"]) for d in state_districts.values()),
            "boundary_type": "SYNTHETIC_STATE_ENVELOPE",
            "crs": config.CRS_NAME,
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Generated synthetic state envelope for Land Stack demonstration"
        }
        states_rows.append(state_props)
        states_features.append({
            "type": "Feature",
            "properties": state_props,
            "geometry": mapping(state_poly)
        })
        
    # Write GeoJSON files
    with open(admin_dir / "states.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": states_features}, f, indent=2)
        
    with open(admin_dir / "districts.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": districts_features}, f, indent=2)
        
    with open(admin_dir / "villages.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": villages_features}, f, indent=2)
        
    # Write CSV files
    pd.DataFrame(states_rows).to_csv(admin_dir / "states.csv", index=False)
    pd.DataFrame(districts_rows).to_csv(admin_dir / "districts.csv", index=False)
    pd.DataFrame(villages_rows).to_csv(admin_dir / "villages.csv", index=False)
    
    print(f"  -> Generated 3 states, 15 districts, 75 villages in {admin_dir}")

if __name__ == "__main__":
    generate_administrative_layers()
