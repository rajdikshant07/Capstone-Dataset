"""
02_generate_parcels.py
Generates 5,250 synthetic land parcels across 3 states, 15 districts, 75 villages.
Outputs:
- parcels.geojson
- parcels.csv
- parcel_attributes.csv
- parcel_geometry_metadata.csv
"""

import sys
import os
import json
import random
import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from shapely.geometry import Point, MultiPoint, Polygon, box, mapping
from shapely.ops import voronoi_diagram
from shapely.validation import make_valid
import pyproj

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config
sys.path.append(str(config.ULPIN_DIR))
from ulpin_generator import SimulatedULPINGenerator

def generate_parcels():
    print("[2/20] Generating 5,250 Synthetic Land Parcels with Realistic Cadastral Geometry...")
    random.seed(config.RANDOM_SEED)
    np.random.seed(config.RANDOM_SEED)
    
    parcel_dir = config.DATA_ACQ_DIR / "Parcel_Data"
    parcel_dir.mkdir(parents=True, exist_ok=True)
    
    ulpin_gen = SimulatedULPINGenerator(seed=config.RANDOM_SEED)
    geod = pyproj.Geod(ellps='WGS84')
    
    parcels_features = []
    parcels_all_rows = []
    parcels_attr_rows = []
    parcels_geom_meta_rows = []
    
    global_parcel_counter = 1
    
    for state_id, state_info in config.ADMIN_HIERARCHY.items():
        state_code = state_info["state_code"]
        state_name = state_info["state_name"]
        
        for dist_id, dist_info in state_info["districts"].items():
            dist_code = dist_info["district_code"]
            dist_name = dist_info["district_name"]
            dist_lat = dist_info["lat"]
            dist_lon = dist_info["lon"]
            
            for v_info in dist_info["villages"]:
                vil_id = v_info["village_id"]
                vil_code = v_info["village_code"]
                vil_name = v_info["village_name"]
                vil_type = v_info["village_type"]
                v_lat = round(dist_lat + v_info["lat_offset"], 6)
                v_lon = round(dist_lon + v_info["lon_offset"], 6)
                
                # Village cadastral extent: approx 0.018 deg lat (~2.0 km) by 0.020 deg lon (~2.1 km)
                delta_lon = 0.010
                delta_lat = 0.009
                vil_box = box(v_lon - delta_lon, v_lat - delta_lat, v_lon + delta_lon, v_lat + delta_lat)
                
                # Generate 70 seed points clustered into:
                # - Core (village abadi): 28 points tightly packed around center (residential, commercial, mixed)
                # - Intermediate: 22 points (peri-urban residential, institutional, light industrial)
                # - Periphery: 20 points widely spaced (agricultural, forest, vacant)
                points = []
                # Core points (radius < 0.003 deg ~ 300m)
                for _ in range(28):
                    r = np.random.uniform(0.0003, 0.0032)
                    theta = np.random.uniform(0, 2 * np.pi)
                    pt_lon = v_lon + r * np.cos(theta) * 1.1
                    pt_lat = v_lat + r * np.sin(theta)
                    points.append(Point(pt_lon, pt_lat))
                    
                # Intermediate points (0.0032 to 0.0068 deg)
                for _ in range(22):
                    r = np.random.uniform(0.0032, 0.0068)
                    theta = np.random.uniform(0, 2 * np.pi)
                    pt_lon = v_lon + r * np.cos(theta) * 1.1
                    pt_lat = v_lat + r * np.sin(theta)
                    points.append(Point(pt_lon, pt_lat))
                    
                # Peripheral points (0.0068 to 0.0095 deg)
                for _ in range(20):
                    r = np.random.uniform(0.0068, 0.0095)
                    theta = np.random.uniform(0, 2 * np.pi)
                    pt_lon = v_lon + r * np.cos(theta) * 1.1
                    pt_lat = v_lat + r * np.sin(theta)
                    points.append(Point(pt_lon, pt_lat))
                    
                mp = MultiPoint(points)
                # Generate Voronoi diagram clipped to village box
                vor = voronoi_diagram(mp, envelope=vil_box)
                
                # Extract and clean polygons
                raw_polys = []
                for g in vor.geoms:
                    inter = g.intersection(vil_box)
                    if inter.is_empty:
                        continue
                    if inter.geom_type == 'Polygon':
                        raw_polys.append(inter)
                    elif inter.geom_type == 'MultiPolygon':
                        for sub_p in inter.geoms:
                            if sub_p.area > 1e-9:
                                raw_polys.append(sub_p)
                                
                # Sort polygons by distance of centroid to village center
                raw_polys.sort(key=lambda p: p.centroid.distance(Point(v_lon, v_lat)))
                
                # Take exactly 70 polygons
                if len(raw_polys) >= config.TARGET_PARCELS_PER_VILLAGE:
                    selected_polys = raw_polys[:config.TARGET_PARCELS_PER_VILLAGE]
                else:
                    # In rare cases, supplement by subdividing the largest polygon
                    selected_polys = list(raw_polys)
                    while len(selected_polys) < config.TARGET_PARCELS_PER_VILLAGE:
                        selected_polys.sort(key=lambda p: p.area, reverse=True)
                        largest = selected_polys.pop(0)
                        minx, miny, maxx, maxy = largest.bounds
                        midx = (minx + maxx) / 2
                        b1 = box(minx, miny, midx, maxy)
                        b2 = box(midx, miny, maxx, maxy)
                        p1 = largest.intersection(b1)
                        p2 = largest.intersection(b2)
                        selected_polys.extend([p1, p2])
                    selected_polys = selected_polys[:config.TARGET_PARCELS_PER_VILLAGE]
                    
                # Process each parcel
                for p_idx, poly in enumerate(selected_polys, start=1):
                    # Validate geometry
                    if not poly.is_valid:
                        poly = make_valid(poly)
                        if poly.geom_type == 'MultiPolygon':
                            poly = max(poly.geoms, key=lambda g: g.area)
                            
                    # Calculate geodesic area and perimeter
                    area_m2, perim_m = geod.geometry_area_perimeter(poly)
                    area_sq_m = round(abs(area_m2), 2)
                    area_ha = round(area_sq_m / 10000.0, 4)
                    perimeter_m = round(abs(perim_m), 2)
                    
                    cent = poly.centroid
                    cent_lat = round(cent.y, 6)
                    cent_lon = round(cent.x, 6)
                    
                    parcel_id = f"PRCL_{state_code}_{dist_code}_{vil_code}_{p_idx:04d}"
                    parcel_num = p_idx
                    
                    # Distance from village center determines land use distribution
                    dist_to_center_km = cent.distance(Point(v_lon, v_lat)) * 111.0
                    
                    if dist_to_center_km < 0.35:
                        # Inner Core
                        l_use = random.choices(
                            ["Residential", "Commercial", "Mixed Use", "Government"],
                            weights=[50, 25, 20, 5], k=1
                        )[0]
                        l_type = "Non-Agricultural"
                    elif dist_to_center_km < 0.75:
                        # Intermediate
                        l_use = random.choices(
                            ["Residential", "Industrial", "Government", "Agricultural", "Vacant Land"],
                            weights=[45, 15, 10, 20, 10], k=1
                        )[0]
                        l_type = "Agricultural" if l_use == "Agricultural" else "Non-Agricultural"
                    else:
                        # Outer Cadastral Fringe
                        l_use = random.choices(
                            ["Agricultural", "Forest", "Vacant Land"],
                            weights=[80, 12, 8], k=1
                        )[0]
                        l_type = "Forest Land" if l_use == "Forest" else "Agricultural"
                        
                    # State-specific survey number formatting
                    if state_id == "MH":
                        gat_base = ((p_idx - 1) // 3) + 1
                        sub_part = (p_idx % 3) + 1
                        survey_num = f"Gat No. {gat_base}"
                        sub_survey_num = f"{sub_part}"
                    elif state_id == "PB":
                        mustatil = ((p_idx - 1) // 8) + 1
                        kila = ((p_idx - 1) % 8) + 1
                        survey_num = f"Khasra No. {mustatil}"
                        sub_survey_num = f"{kila}//1"
                    else: # GJ
                        block_base = ((p_idx - 1) // 2) + 1
                        sub_part = f"P{(p_idx % 2) + 1}"
                        survey_num = f"Block No. {block_base}"
                        sub_survey_num = sub_part
                        
                    # Generate deterministic simulated ULPIN
                    sim_ulpin, _ = ulpin_gen.generate_ulpin(
                        state_code=state_code,
                        district_code=dist_code,
                        village_code=vil_code,
                        centroid_lat=cent_lat,
                        centroid_lon=cent_lon,
                        parcel_seq=p_idx
                    )
                    
                    rec_status = random.choices(
                        ["Active", "Mutated", "Under_Dispute", "Subdivided"],
                        weights=[88, 7, 3, 2], k=1
                    )[0]
                    
                    created_date = (datetime.date(2021, 1, 1) + datetime.timedelta(days=random.randint(0, 900))).isoformat()
                    updated_date = (datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 300))).isoformat()
                    
                    # Coordinate bounds
                    min_x, min_y, max_x, max_y = poly.bounds
                    
                    props = {
                        "parcel_id": parcel_id,
                        "state_id": state_id,
                        "state_name": state_name,
                        "district_id": dist_id,
                        "district_name": dist_name,
                        "village_id": vil_id,
                        "village_name": vil_name,
                        "survey_number": survey_num,
                        "sub_survey_number": sub_survey_num,
                        "parcel_number": parcel_num,
                        "land_type": l_type,
                        "land_use_category": l_use,
                        "area_sq_m": area_sq_m,
                        "area_hectares": area_ha,
                        "perimeter_m": perimeter_m,
                        "centroid_latitude": cent_lat,
                        "centroid_longitude": cent_lon,
                        "simulated_ulpin": sim_ulpin,
                        "record_status": rec_status,
                        "created_at": created_date,
                        "updated_at": updated_date,
                        "data_status": config.DATA_STATUS["SYNTHETIC"]
                    }
                    
                    geom_mapping = mapping(poly)
                    parcels_features.append({
                        "type": "Feature",
                        "properties": props,
                        "geometry": geom_mapping
                    })
                    
                    # Full CSV row (including WKT geometry)
                    row_full = dict(props)
                    row_full["geometry_wkt"] = poly.wkt
                    parcels_all_rows.append(row_full)
                    
                    # Attribute table (without geometry for fast relational indexing)
                    parcels_attr_rows.append(props)
                    
                    # Geometry metadata table
                    parcels_geom_meta_rows.append({
                        "parcel_id": parcel_id,
                        "simulated_ulpin": sim_ulpin,
                        "geometry_type": poly.geom_type,
                        "num_vertices": len(poly.exterior.coords),
                        "is_valid": poly.is_valid,
                        "is_simple": poly.is_simple,
                        "is_closed": poly.exterior.is_closed,
                        "bbox_min_lon": round(min_x, 6),
                        "bbox_min_lat": round(min_y, 6),
                        "bbox_max_lon": round(max_x, 6),
                        "bbox_max_lat": round(max_y, 6),
                        "geodesic_area_sq_m": area_sq_m,
                        "geodesic_perimeter_m": perimeter_m,
                        "crs": config.CRS_NAME,
                        "verification_status": "VALID"
                    })
                    
                    global_parcel_counter += 1
                    
    # Write GeoJSON
    print(f"  -> Writing parcels.geojson ({len(parcels_features)} features)...")
    geojson_obj = {
        "type": "FeatureCollection",
        "name": "LandStack_Synthetic_Cadastral_Parcels",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": parcels_features
    }
    with open(parcel_dir / "parcels.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson_obj, f)
        
    # Write CSVs
    print("  -> Writing parcels.csv, parcel_attributes.csv, and parcel_geometry_metadata.csv...")
    pd.DataFrame(parcels_all_rows).to_csv(parcel_dir / "parcels.csv", index=False)
    pd.DataFrame(parcels_attr_rows).to_csv(parcel_dir / "parcel_attributes.csv", index=False)
    pd.DataFrame(parcels_geom_meta_rows).to_csv(parcel_dir / "parcel_geometry_metadata.csv", index=False)
    
    print(f"  -> SUCCESS: Generated {len(parcels_all_rows)} parcels across {len(config.ADMIN_HIERARCHY)} states.")
    return parcels_attr_rows

if __name__ == "__main__":
    generate_parcels()
