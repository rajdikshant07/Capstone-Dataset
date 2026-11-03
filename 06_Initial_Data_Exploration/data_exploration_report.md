# Land Stack: Initial Data Exploration & Statistical Profiling Report

## Module 1: Data Acquisition and Dataset Preparation
**Generated On:** 2026-11-02 19:02:16 UTC  
**Coordinate Reference System:** `EPSG:4326 (WGS 84 - 2D Geographic Coordinate Reference System)`  
**Random Generation Seed:** `42`

---

## 1. Executive Summary

This exploratory data analysis report provides a comprehensive review of the synthetic spatial and departmental datasets prepared for **Module 1** of the Land Stack Digital Public Infrastructure platform.

All datasets were synthesized programmatically using reproducible geometric and statistical modeling techniques in Python. The dataset package establishes the foundational layer required for subsequent extract-transform-load (ETL), spatial relational modeling (PostgreSQL/PostGIS), vector tile serving, and public service delivery APIs.

---

## 2. Dataset Ingestion & Volume Metrics

| Dataset Name | Record Count | Storage Format | Primary Identifier | Spatial Geometry |
|---|---|---|---|---|
| **Cadastral Land Parcels** | 5,250 | GeoJSON, CSV | `parcel_id` | Polygon (Cadastral Cadastre) |
| **Simulated ULPIN Records** | 5,250 | CSV, JSON | `ulpin` | Linked to Parcel Centroids |
| **Land Use & Land Cover** | 5,250 | GeoJSON, CSV | `land_use_id` | Polygon (Zonal Overlay) |
| **Road Network Alignments** | 375 | GeoJSON, CSV | `road_id` | LineString (Road Centerlines) |
| **Hydrological Water Bodies** | 105 | GeoJSON, CSV | `waterbody_id` | Polygon / LineString |
| **Utility Infrastructure Assets** | 900 | GeoJSON, CSV | `utility_id` | Point / LineString |
| **Ownership Title Registry** | 6,748 | CSV | `owner_id` | Tabular (FK: `parcel_id`) |
| **Record of Rights (RoR Extracts)** | 5,250 | CSV | `ror_id` | Tabular (FK: `parcel_id`) |
| **Property Registration Deeds** | 2,500 | CSV | `registration_id` | Tabular (FK: `parcel_id`) |
| **Property Tax Assessments** | 10,500 | CSV | `tax_id` | Tabular (FK: `parcel_id`) |
| **Mortgages & Encumbrances** | 1,250 | CSV | `encumbrance_id` | Tabular (FK: `parcel_id`) |
| **Building Permits & Sanctions** | 950 | CSV | `permit_id` | Tabular (FK: `parcel_id`) |
| **Land Restrictions & Injunctions** | 450 | GeoJSON, CSV | `restriction_id` | Polygon Overlay |
| **Audit & Change History Trail** | 3,500 | CSV | `audit_id` | Tabular (FK: `parcel_id`) |

---

## 3. Spatial Geometry & Coordinate System Integrity

- **Coordinate System Validation:** All spatial layers are explicitly standardized to EPSG:4326 (WGS 84 2D coordinates: `[longitude, latitude]`).
- **Polygon Validity Inspection:** Evaluated using Shapely topology assertions.
  - Total polygon rings evaluated: **5,250**
  - Self-intersecting rings detected: **0 (0.0%)**
  - Closed boundary rings: **100% verified**
  - Unclosed or degenerate geometries: **0 (0.0%)**
- **Geodesic Accuracy:** Parcel areas and perimeters were computed using ellipsoidal geodesic metrics (`pyproj.Geod` on WGS 84 ellipsoid), strictly avoiding degree-square distortion errors.
- **Metric Projection Guidance for PostGIS:** When ingesting into PostGIS in Module 3, parcel geometries must be projected into UTM Zone 43N (`EPSG:32643`) or local state plane projections for sub-meter planar calculations.

---

## 4. Cadastral Parcel Characteristics & Area Statistics

- **Minimum Parcel Area:** 214.14 m² (0.0214 Ha)
- **Maximum Parcel Area:** 470,582.41 m² (47.0582 Ha)
- **Mean Parcel Area:** 57,667.73 m² (5.7668 Ha)
- **Median Parcel Area:** 39,337.07 m² (3.9337 Ha)
- **Standard Deviation:** 57,284.92 m²

### Geographic Distribution
- **Maharashtra:** 1,750 parcels across 5 districts (Pune, Nagpur, Nashik, Chhatrapati Sambhajinagar, Kolhapur)
- **Punjab:** 1,750 parcels across 5 districts (Amritsar, Ludhiana, Jalandhar, Patiala, Bathinda)
- **Gujarat:** 1,750 parcels across 5 districts (Ahmedabad, Surat, Vadodara, Rajkot, Gandhinagar)

---

## 5. Foreign Key & Relational Consistency Verification

| Child Table | Parent Reference | Expected Keys | Resolved Valid Keys | Broken References | Integrity Status |
|---|---|---|---|---|---|
| `ownership_records` | `parcels(parcel_id)` | 6,748 | 6,748 | 0 | **100% PASS** |
| `ror_records` | `parcels(parcel_id)` | 5,250 | 5,250 | 0 | **100% PASS** |
| `property_registration` | `parcels(parcel_id)` | 2,500 | 2,500 | 0 | **100% PASS** |
| `property_tax` | `parcels(parcel_id)` | 10,500 | 10,500 | 0 | **100% PASS** |
| `mortgages_encumbrances` | `parcels(parcel_id)` | 1,250 | 1,250 | 0 | **100% PASS** |
| `building_permits` | `parcels(parcel_id)` | 950 | 950 | 0 | **100% PASS** |
| `land_restrictions` | `parcels(parcel_id)` | 450 | 450 | 0 | **100% PASS** |
| `audit_history` | `parcels(parcel_id)` | 3,500 | 3,500 | 0 | **100% PASS** |

---

## 6. Generated Visual Analytics

The following charts were generated and saved in the `06_Initial_Data_Exploration/charts/` directory:
1. `parcels_by_state.png` - State-wise parcel distribution.
2. `parcels_by_district.png` - District-level breakdown across 15 districts.
3. `land_use_distribution.png` - Functional land use category frequencies.
4. `parcel_area_distribution.png` - Histogram of parcel areas with mean and median indicators.
5. `ownership_distribution.png` - Donut chart of ownership types (Individual, Joint, Corporate, Government, Trust).
6. `departmental_records_distribution.png` - Volume comparison of departmental records linked via ULPIN.

*Conclusion: The dataset package satisfies all structural, relational, and geometric integrity requirements established for Module 1.*
