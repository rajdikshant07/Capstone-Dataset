"""
06_generate_roads.py
Generates synthetic road network connecting villages and district settlements:
- 01_Data_Acquisition/Roads/roads.geojson
- 01_Data_Acquisition/Roads/roads.csv
"""

import sys
import os
import json
import random
from pathlib import Path
import pandas as pd
from shapely.geometry import LineString, Point, mapping
import pyproj

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_roads():
    print("[6/20] Generating Synthetic Road Network (Highways, District Roads, Village Access Roads)...")
    random.seed(config.RANDOM_SEED)
    
    roads_dir = config.DATA_ACQ_DIR / "Roads"
    roads_dir.mkdir(parents=True, exist_ok=True)
    
    geod = pyproj.Geod(ellps='WGS84')
    
    road_features = []
    road_rows = []
    road_counter = 1
    
    for state_id, state_info in config.ADMIN_HIERARCHY.items():
        state_name = state_info["state_name"]
        
        for dist_id, dist_info in state_info["districts"].items():
            dist_name = dist_info["district_name"]
            dist_lat = dist_info["lat"]
            dist_lon = dist_info["lon"]
            hq_pt = (dist_lon, dist_lat)
            
            villages = dist_info["villages"]
            vil_coords = []
            
            # 1. District arterial Highway passing near HQ
            hwy_id = f"RD_{state_id}_{road_counter:05d}"
            road_counter += 1
            hwy_line = LineString([
                (dist_lon - 0.22, dist_lat - 0.08),
                (dist_lon - 0.05, dist_lat - 0.02),
                (dist_lon + 0.08, dist_lat + 0.04),
                (dist_lon + 0.24, dist_lat + 0.12)
            ])
            _, hwy_len = geod.geometry_area_perimeter(hwy_line)
            hwy_props = {
                "road_id": hwy_id,
                "road_name": f"{state_name} Arterial Highway Corridor {dist_name}",
                "state_id": state_id,
                "state_name": state_name,
                "district_id": dist_id,
                "district_name": dist_name,
                "village_id": "REGIONAL_CORRIDOR",
                "village_name": "Multiple Jurisdictions",
                "road_category": "State Highway",
                "road_surface": "Bituminous (Asphalt)",
                "road_width_m": 14.0,
                "road_length_m": round(abs(hwy_len), 2),
                "connectivity_info": f"Interconnects {dist_name} HQ with state transport spine",
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic road centerline alignment for demonstration"
            }
            road_rows.append(hwy_props)
            road_features.append({"type": "Feature", "properties": hwy_props, "geometry": mapping(hwy_line)})
            
            # 2. Radiating Major District Roads from HQ to each Village
            for v_info in villages:
                v_lat = round(dist_lat + v_info["lat_offset"], 6)
                v_lon = round(dist_lon + v_info["lon_offset"], 6)
                vil_coords.append((v_info["village_id"], v_info["village_name"], v_lon, v_lat))
                
                # Connector road HQ -> Village
                mdr_id = f"RD_{state_id}_{road_counter:05d}"
                road_counter += 1
                # Add a realistic midpoint bend
                mid_lon = (dist_lon + v_lon) / 2 + random.uniform(-0.008, 0.008)
                mid_lat = (dist_lat + v_lat) / 2 + random.uniform(-0.008, 0.008)
                mdr_line = LineString([hq_pt, (mid_lon, mid_lat), (v_lon, v_lat)])
                _, mdr_len = geod.geometry_area_perimeter(mdr_line)
                
                mdr_props = {
                    "road_id": mdr_id,
                    "road_name": f"{dist_name}-{v_info['village_name']} District Link",
                    "state_id": state_id,
                    "state_name": state_name,
                    "district_id": dist_id,
                    "district_name": dist_name,
                    "village_id": v_info["village_id"],
                    "village_name": v_info["village_name"],
                    "road_category": "District Road",
                    "road_surface": "Bituminous (Asphalt)",
                    "road_width_m": 7.5,
                    "road_length_m": round(abs(mdr_len), 2),
                    "connectivity_info": f"Connects {dist_name} headquarters to {v_info['village_name']}",
                    "data_status": config.DATA_STATUS["SYNTHETIC"],
                    "provenance": "Synthetic district link road for Land Stack simulation"
                }
                road_rows.append(mdr_props)
                road_features.append({"type": "Feature", "properties": mdr_props, "geometry": mapping(mdr_line)})
                
                # 3. Village Internal Roads and Cadastral Access Pathways (3 per village)
                for r_sub in range(1, 4):
                    vr_id = f"RD_{state_id}_{road_counter:05d}"
                    road_counter += 1
                    dx = 0.008 * (1 if r_sub == 1 else (-1 if r_sub == 2 else 0.5))
                    dy = 0.007 * (1 if r_sub == 2 else (-0.7 if r_sub == 1 else -1))
                    
                    vr_cat = "Village Road" if r_sub < 3 else "Local Road"
                    surf = "Concrete" if r_sub == 1 else ("Bituminous" if r_sub == 2 else "WBM (Gravel/Earthen)")
                    width = 5.5 if r_sub == 1 else 3.75
                    
                    vr_line = LineString([
                        (v_lon - dx * 0.7, v_lat - dy * 0.7),
                        (v_lon, v_lat),
                        (v_lon + dx * 0.9, v_lat + dy * 0.8)
                    ])
                    _, vr_len = geod.geometry_area_perimeter(vr_line)
                    
                    vr_props = {
                        "road_id": vr_id,
                        "road_name": f"{v_info['village_name']} Cadastral Access Sector {r_sub}",
                        "state_id": state_id,
                        "state_name": state_name,
                        "district_id": dist_id,
                        "district_name": dist_name,
                        "village_id": v_info["village_id"],
                        "village_name": v_info["village_name"],
                        "road_category": vr_cat,
                        "road_surface": surf,
                        "road_width_m": width,
                        "road_length_m": round(abs(vr_len), 2),
                        "connectivity_info": f"Serves interior farm parcels and abadi of {v_info['village_name']}",
                        "data_status": config.DATA_STATUS["SYNTHETIC"],
                        "provenance": "Synthetic village internal access network"
                    }
                    road_rows.append(vr_props)
                    road_features.append({"type": "Feature", "properties": vr_props, "geometry": mapping(vr_line)})
                    
            # 4. Inter-village connector road linking village 1 -> 2 -> 3
            for i in range(len(vil_coords) - 1):
                iv_id = f"RD_{state_id}_{road_counter:05d}"
                road_counter += 1
                v1 = vil_coords[i]
                v2 = vil_coords[i+1]
                iv_line = LineString([(v1[2], v1[3]), (v2[2], v2[3])])
                _, iv_len = geod.geometry_area_perimeter(iv_line)
                iv_props = {
                    "road_id": iv_id,
                    "road_name": f"{v1[1]}-{v2[1]} Rural Connector",
                    "state_id": state_id,
                    "state_name": state_name,
                    "district_id": dist_id,
                    "district_name": dist_name,
                    "village_id": f"{v1[0]}+{v2[0]}",
                    "village_name": f"{v1[1]} - {v2[1]}",
                    "road_category": "Village Road",
                    "road_surface": "Bituminous (Asphalt)",
                    "road_width_m": 5.5,
                    "road_length_m": round(abs(iv_len), 2),
                    "connectivity_info": f"Inter-village connectivity between {v1[1]} and {v2[1]}",
                    "data_status": config.DATA_STATUS["SYNTHETIC"],
                    "provenance": "Synthetic inter-village link"
                }
                road_rows.append(iv_props)
                road_features.append({"type": "Feature", "properties": iv_props, "geometry": mapping(iv_line)})
                
    # Save GeoJSON
    with open(roads_dir / "roads.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": road_features}, f, indent=2)
        
    # Save CSV
    pd.DataFrame(road_rows).to_csv(roads_dir / "roads.csv", index=False)
    print(f"  -> Generated {len(road_rows)} road segments in {roads_dir}")

if __name__ == "__main__":
    generate_roads()
