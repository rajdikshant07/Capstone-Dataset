"""
07_generate_water_bodies.py
Generates synthetic water body geometries (Rivers, Canals, Lakes, Ponds, Reservoirs):
- 01_Data_Acquisition/Water_Bodies/water_bodies.geojson
- 01_Data_Acquisition/Water_Bodies/water_bodies.csv
"""

import sys
import os
import json
import random
import math
from pathlib import Path
import pandas as pd
from shapely.geometry import Polygon, LineString, Point, box, mapping
from shapely.validation import make_valid
import pyproj

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_water_bodies():
    print("[7/20] Generating Synthetic Water Bodies (Rivers, Canals, Lakes, Ponds, Reservoirs)...")
    random.seed(config.RANDOM_SEED)
    
    wb_dir = config.DATA_ACQ_DIR / "Water_Bodies"
    wb_dir.mkdir(parents=True, exist_ok=True)
    
    geod = pyproj.Geod(ellps='WGS84')
    
    wb_features = []
    wb_rows = []
    wb_counter = 1
    
    for state_id, state_info in config.ADMIN_HIERARCHY.items():
        state_name = state_info["state_name"]
        
        for dist_id, dist_info in state_info["districts"].items():
            dist_name = dist_info["district_name"]
            dist_lat = dist_info["lat"]
            dist_lon = dist_info["lon"]
            
            # 1. District Major River / Reservoir Corridor (Polygon or LineString)
            r_id = f"WB_{state_id}_{wb_counter:05d}"
            wb_counter += 1
            # River poly ribbon
            river_pts = [
                (dist_lon - 0.20, dist_lat + 0.15),
                (dist_lon - 0.05, dist_lat + 0.08),
                (dist_lon + 0.10, dist_lat - 0.02),
                (dist_lon + 0.22, dist_lat - 0.12)
            ]
            river_line = LineString(river_pts)
            # Buffer by ~150 meters (0.0014 deg) to make realistic polygon river channel
            river_poly = river_line.buffer(0.0014)
            area_m2, perim_m = geod.geometry_area_perimeter(river_poly)
            
            r_props = {
                "waterbody_id": r_id,
                "waterbody_name": f"{dist_name} Main Drainage River",
                "state_id": state_id,
                "state_name": state_name,
                "district_id": dist_id,
                "district_name": dist_name,
                "village_id": "REGIONAL_BASIN",
                "village_name": "Multiple Jurisdictions",
                "waterbody_type": "River",
                "geometry_type": "Polygon",
                "perennial_status": "Perennial",
                "approx_area_sq_m": round(abs(area_m2), 2),
                "approx_length_m": round(abs(perim_m) / 2, 2),
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic river channel envelope for spatial buffer queries"
            }
            wb_rows.append(r_props)
            wb_features.append({"type": "Feature", "properties": r_props, "geometry": mapping(river_poly)})
            
            # 2. Main Irrigation Branch Canal
            c_id = f"WB_{state_id}_{wb_counter:05d}"
            wb_counter += 1
            canal_line = LineString([
                (dist_lon - 0.15, dist_lat - 0.18),
                (dist_lon + 0.02, dist_lat - 0.05),
                (dist_lon + 0.18, dist_lat + 0.10)
            ])
            _, canal_len = geod.geometry_area_perimeter(canal_line)
            c_props = {
                "waterbody_id": c_id,
                "waterbody_name": f"{dist_name} Left Bank Irrigation Canal",
                "state_id": state_id,
                "state_name": state_name,
                "district_id": dist_id,
                "district_name": dist_name,
                "village_id": "DISTRICT_CANAL_NETWORK",
                "village_name": "Multiple Jurisdictions",
                "waterbody_type": "Canal",
                "geometry_type": "LineString",
                "perennial_status": "Seasonal / Controlled Flow",
                "approx_area_sq_m": round(canal_len * 8.0, 2), # ~8m canal bed
                "approx_length_m": round(abs(canal_len), 2),
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic irrigation canal network centerline"
            }
            wb_rows.append(c_props)
            wb_features.append({"type": "Feature", "properties": c_props, "geometry": mapping(canal_line)})
            
            # 3. Village Water Bodies (Village Pond / Lake / Percolation Tank per village)
            for v_info in dist_info["villages"]:
                v_lat = round(dist_lat + v_info["lat_offset"], 6)
                v_lon = round(dist_lon + v_info["lon_offset"], 6)
                
                # Village Community Pond
                p_id = f"WB_{state_id}_{wb_counter:05d}"
                wb_counter += 1
                
                # Elliptical / irregular polygon pond with proper trigonometric vertices
                pond_center_lon = v_lon + 0.007
                pond_center_lat = v_lat - 0.006
                angles = [0, 45, 90, 135, 180, 225, 270, 315]
                poly_coords = []
                for a in angles:
                    rad = random.uniform(0.0010, 0.0018)
                    rad_x = rad * (1.25 if a in [0, 180] else 0.85)
                    rad_y = rad * (0.85 if a in [0, 180] else 1.15)
                    rad_angle = math.radians(a)
                    x = pond_center_lon + rad_x * math.cos(rad_angle)
                    y = pond_center_lat + rad_y * math.sin(rad_angle)
                    poly_coords.append((round(x, 6), round(y, 6)))
                poly_coords.append(poly_coords[0])
                pond_poly = Polygon(poly_coords)
                if not pond_poly.is_valid:
                    pond_poly = make_valid(pond_poly)
                    if pond_poly.geom_type == 'MultiPolygon':
                        pond_poly = max(pond_poly.geoms, key=lambda g: g.area)
                p_area_m2, p_perim_m = geod.geometry_area_perimeter(pond_poly)
                
                pond_type = random.choice(["Pond", "Lake", "Reservoir"])
                p_props = {
                    "waterbody_id": p_id,
                    "waterbody_name": f"{v_info['village_name']} Gram Panchayat {pond_type}",
                    "state_id": state_id,
                    "state_name": state_name,
                    "district_id": dist_id,
                    "district_name": dist_name,
                    "village_id": v_info["village_id"],
                    "village_name": v_info["village_name"],
                    "waterbody_type": pond_type,
                    "geometry_type": "Polygon",
                    "perennial_status": "Semi-Perennial",
                    "approx_area_sq_m": round(abs(p_area_m2), 2),
                    "approx_length_m": round(abs(p_perim_m), 2),
                    "data_status": config.DATA_STATUS["SYNTHETIC"],
                    "provenance": "Synthetic village water tank for spatial overlay"
                }
                wb_rows.append(p_props)
                wb_features.append({"type": "Feature", "properties": p_props, "geometry": mapping(pond_poly)})
                
    # Save GeoJSON
    with open(wb_dir / "water_bodies.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": wb_features}, f, indent=2)
        
    # Save CSV
    pd.DataFrame(wb_rows).to_csv(wb_dir / "water_bodies.csv", index=False)
    print(f"  -> Generated {len(wb_rows)} water body features in {wb_dir}")

if __name__ == "__main__":
    generate_water_bodies()
