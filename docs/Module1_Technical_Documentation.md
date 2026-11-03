# Land Stack: Technical Documentation
## Module 1 – Data Acquisition and Dataset Preparation
### Report 3: Geospatial Database and Data Engineering
**Author:** Land Stack Data Engineering & GIS Architecture Team  
**Project:** Integrated GIS-Based Digital Public Infrastructure for Land Governance (Final Year B.Tech CSE Capstone)  
**Version:** 1.0.0 (Release Candidate)  
**Status:** Validated & Complete  

---

## 1. Module 1 Purpose and Strategic Scope

In India, land governance data is fragmented across isolated departmental silos:
- Revenue departments manage cadastre maps, Records of Rights (RoRs), and tenant ledgers.
- Registration departments maintain deed records and stamp duty assessments.
- Local planning and municipal authorities manage building permits, master plans, and property taxes.
- Financial institutions register mortgages and equitable liens.
- Courts issue civil injunctions and status-quo stay orders.
- Environmental and forest agencies enforce regulatory buffers and conservation corridors.

This fragmentation leads to opaque property transactions, duplicate sales, litigation backlogs, and substantial credit friction.

**Land Stack** addresses this challenge by establishing an integrated, GIS-based Digital Public Infrastructure (DPI) for land administration across India. The objective of **Module 1 (Data Acquisition and Dataset Preparation)** is to engineer a realistic, standardized, and cross-state synthetic geospatial dataset foundation. This dataset acts as the testbed and benchmark for subsequent extract-transform-load (ETL) processing, PostgreSQL/PostGIS spatial modeling, ULPIN resolution, vector tile serving, and public service APIs.

---

## 2. Multi-State Geographic Coverage Strategy

To prove that Land Stack is India-wide and not tied to the administrative conventions of a single state or city, Module 1 models three culturally and administratively distinct states:

| State | State Code (LGD) | Sample Districts | Sample Villages | Total Parcels | Dominant Land Record System |
|---|---|---|---|---|---|
| **Maharashtra** | `27` | Pune, Nagpur, Nashik, Chhatrapati Sambhajinagar, Kolhapur | 25 Villages (5 / district) | 1,750 | Mahabhulekh (Gat No., 7/12 Extract, 8A Khata, Ferfar) |
| **Punjab** | `03` | Amritsar, Ludhiana, Jalandhar, Patiala, Bathinda | 25 Villages (5 / district) | 1,750 | PLRS (Khasra No., Murabba/Kila, Jamabandi, Inteqal) |
| **Gujarat** | `24` | Ahmedabad, Surat, Vadodara, Rajkot, Gandhinagar | 25 Villages (5 / district) | 1,750 | AnyRoR (Block No., VF-7/12, VF-8A, Hakk Patrak) |
| **Total** | **3 States** | **15 Districts** | **75 Villages** | **5,250 Parcels** | **Unified Common Schema** |

The hierarchy is structured deterministically:
$$\text{State (3)} \longrightarrow \text{Districts (15)} \longrightarrow \text{Villages (75)} \longrightarrow \text{Parcels (5,250)}$$

---

## 3. Coordinate Reference System (CRS) Strategy

### 3.1 Data Interchange Format: WGS 84 (EPSG:4326)
All vector geometry files (`parcels.geojson`, `roads.geojson`, `water_bodies.geojson`, `utilities.geojson`, `land_use.geojson`, `land_restrictions.geojson`) are standardized in **EPSG:4326 (WGS 84 2D geographic coordinates)** with coordinates ordered as `[longitude, latitude]`. This ensures broad compatibility with modern web GIS frameworks (MapLibre GL, OpenLayers, Leaflet), desktop GIS software (QGIS, ArcGIS Pro), and cloud data warehouses.

### 3.2 Geodesic Area and Distance Calculation
Calculating parcel areas or road lengths directly in decimal degrees using spherical approximations produces severe distortion across different latitudes. Module 1 computes all geometric metrics geodesically on the WGS 84 reference ellipsoid using `pyproj.Geod(ellps='WGS84')`:
- `area_sq_m`: Exact ellipsoidal geodesic polygon surface area in square meters.
- `area_hectares`: Exact area converted to standard SI hectares ($1\text{ Ha} = 10,000\text{ m}^2$).
- `perimeter_m`: Exact ellipsoidal geodesic perimeter in linear meters.

### 3.3 Guidance for Future PostGIS Ingestion (Module 3)
When ingesting these datasets into PostgreSQL/PostGIS during Module 3:
- Ingest raw geometry as `GEOMETRY(Geometry, 4326)` for global coordinate integrity.
- Create generated columns or spatial indexes using Universal Transverse Mercator (UTM) Zone 43N (`EPSG:32643`) for Maharashtra and Gujarat, and UTM Zone 43N/44N for Punjab:
```sql
ALTER TABLE parcels ADD COLUMN geom_utm geometry(Polygon, 32643) 
GENERATED ALWAYS AS (ST_Transform(geometry, 32643)) STORED;
CREATE INDEX idx_parcels_geom_utm ON parcels USING GIST (geom_utm);
```

---

## 4. Cadastral Parcel Geometry Generation Engine

Real cadastral maps are not uniform grids; they are irregular polygonal mosaics formed by natural features, family partitions, and historical consolidation.

Module 1 implements a **Clipped Voronoi Tessellation Algorithm**:
1. **Zonal Point Seeding:** In each village, 70 seed points are distributed radially around the village centroid:
   - **Village Core / Abadi (0 – 350 m):** High-density clusters producing smaller plots (150 – 1,500 m²) representative of residential, retail, and gram-panchayat institutional lots.
   - **Intermediate Transition Zone (350 – 750 m):** Medium-density points producing plots (500 – 3,500 m²) representative of light industrial units, warehouses, and peri-urban holdings.
   - **Outer Agricultural Cadastral Fringe (750 – 2,000 m):** Sparser seed points producing large polygons (10,000 – 60,000 m², or 1 – 6 hectares) representative of cultivated fields and orchard lands.
2. **Voronoi Diagram Calculation:** Computes the mathematical Voronoi partition from seed points.
3. **Bounding Box Intersection & Topology Cleaning:** Clips Voronoi polygons to the village boundary envelope. Cleans boundaries using `shapely.validation.make_valid` to ensure counter-clockwise outer rings, closed exterior paths, and zero self-intersections.
4. **Guaranteed Gapless & Overlap-Free Structure:** Adjacent parcels share identical edge segments, forming a topology-clean cadastral map.

---

## 5. Simulated ULPIN Generation Engine

The Government of India has introduced the **Unique Land Parcel Identification Number (ULPIN)**, also termed **Bhu-Aadhaar**, as a 14-digit alphanumeric code based on parcel centroid coordinates.

In Module 1, `ulpin_generator.py` implements a deterministic simulation:
- **Digits 1–2:** State LGD code (`27` for MH, `03` for PB, `24` for GJ).
- **Digits 3–4:** District code (`01` through `05`).
- **Digits 5–7:** Village code (`001` through `005`).
- **Digits 8–14:** 7-character Base36 (`0-9, A-Z`) spatial coordinate hash derived from the parcel centroid and seed.

### Collision Resistance Verification
Every generated ULPIN is checked against an in-memory collision registry. Across all 5,250 parcels:
- Duplicate ULPINs detected: **0 (0.0% collision rate)**.
- Re-running with seed 42 produces identical ULPINs, ensuring reproducibility across development and testing environments.

> **Disclaimer:** The identifier format is a simulated project design for DPI demonstration and does not claim compliance with proprietary Survey of India server-side key derivation functions.

---

## 6. Multi-Departmental Relational Architecture

The platform breaks data silos by establishing the `parcel_id` and `simulated_ulpin` as immutable foreign keys across eight departmental tables:

```
                               ┌────────────────────────┐
                               │   parcels.geojson /    │
                               │      parcels.csv       │
                               │  PK: parcel_id, ulpin  │
                               └───────────┬────────────┘
                                           │
         ┌───────────────────┬─────────────┼─────────────┬───────────────────┐
         │                   │             │             │                   │
         ▼                   ▼             ▼             ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────┴─────┐ ┌─────────────────┐ ┌─────┴─────┐
│ownership_records│ │   ror_records   │ │property_  │ │  property_tax   │ │mortgages_   │
│  (6,748 rows)   │ │  (5,250 rows)   │ │registration││ (10,500 rows)  │ │encumbrances │
│Individual/Joint │ │7/12 / Jamabandi │ │(2,500 deeds││FY 23-24 & 24-25 │ │(1,250 loans)│
└─────────────────┘ └─────────────────┘ └───────────┘ └─────────────────┘ └───────────┘
         │                   │                           │                   │
         └─────────────┬─────┴───────────────────────────┴─────────────┬─────┘
                       ▼                                               ▼
              ┌─────────────────┐                             ┌─────────────────┐
              │building_permits │                             │land_restrictions│
              │   (950 rows)    │                             │   (450 rows)    │
              │  Urban Planning │                             │ Court / Forest  │
              └─────────────────┘                             └─────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │     audit_history       │
                              │      (3,500 rows)       │
                              │ Mutation / Split / Ingest│
                              └─────────────────────────┘
```

1. **Ownership Registry (`ownership_records.csv`):** Supports sole ownership (100%), joint ownership with fractional shares (e.g. 50/50, 33.34/33.33/33.33), corporate entities, government departments, and charitable trusts. Uses culturally authentic fictional names per state.
2. **Record of Rights (`ror_records.csv`):** Simulates Maharashtra 7/12 extracts, Punjab Jamabandi Nakals, and Gujarat VF-7/12 forms, capturing irrigation sources, tenancy types, and crop classifications.
3. **Property Registration (`property_registration.csv`):** Simulates Sub-Registrar Office (SRO) deed instruments (Sale, Gift, Inheritance, Lease, Partition, Mortgage) with market valuations, stamp duties, and registration fees.
4. **Property Tax (`property_tax.csv`):** Multi-year tax assessment records across FY 2023-24 and FY 2024-25, tracking demand, collections, penalties, and payment dates.
5. **Mortgages & Encumbrances (`mortgages_encumbrances.csv`):** Financial charges registered by public, private, and agricultural cooperative lending institutions.
6. **Building Permits (`building_permits.csv`):** Planning permissions, floor area ratios, and structural sanctions issued by urban development authorities.
7. **Land Restrictions (`land_restrictions.csv` & `.geojson`):** Statutory encumbrances (environmental buffer zones, highway acquisition notifications, civil court stay orders, forest conservation margins).
8. **Audit Trail (`audit_history.csv`):** Immutable transaction ledger recording operator timestamps, old/new values, and modification justifications.

---

## 7. State Schema Variations & Extensibility Template

The state mapping architecture decouples the core database schema from local state terminology:
- **`state_mapping_template.xlsx` & `.csv`:** Comprehensive dictionary mapping local revenue terms (Gat No., Khasra No., Block No., Hadbast, Khatedar, Kanal-Marla, Hectare-Are) to standard Land Stack attributes.
- **`field_mapping_rules.json`:** Machine-readable transformation rules containing parsing regular expressions, null-handling strategies, and mathematical unit converters.
- **Extensibility to a Fourth State:** Demonstrates how Karnataka (Bhoomi RTC) can be integrated by adding declarative JSON mapping rules without restructuring database tables.

---

## 8. Data Quality Assurance and Validation Framework

`data_quality_checks.py` executes an automated test suite across all generated layers:
1. **Primary Key & Identifier Uniqueness:** Confirms zero duplicate parcel IDs and zero duplicate ULPINs.
2. **Format Adherence:** Verifies all ULPINs match the exact 14-character uppercase alphanumeric specification.
3. **Topological Ring Validity:** Uses Shapely geometry assertions to ensure all polygon rings are closed, non-self-intersecting, and free of spikes or zero-area degeneracies.
4. **Coordinate Boundaries:** Asserts that parcel centroids fall strictly within the geographic bounds of their respective districts and states.
5. **Referential Integrity:** Verifies that 100% of foreign keys in all eight departmental tables successfully resolve to an existing `parcel_id`.
6. **Error Reporting:** Generates `data_quality_report.json`, `data_quality_report.xlsx`, and `validation_errors.csv` (reporting **0 errors / 100.0% compliance**).

---

## 9. Limitations and Boundary Conditions

- **100% Synthetic Nature:** All parcel boundaries, ownership names, deed numbers, and tax figures are computer-generated demonstration records. They must not be cited as legal cadastral evidence.
- **Approximate Geographic Anchors:** Village centroids use approximate public geographic coordinates to ensure parcels cluster realistically within their respective districts.
- **Simulated Satellite LULC:** The land use layer simulates 10m multi-spectral optical classifications; it is not derived from commercial satellite licenses.

---

## 10. Direct Interface with Next Project Modules

- **Module 2 (ETL and Data Cleaning):** Provides raw multi-state tables, state mapping configuration files, and validation error registers to exercise automated ingestion pipelines.
- **Module 3 (Geospatial Database & PostGIS):** Provides clean GeoJSON and CSV tables with known geometry types and primary/foreign key relationships ready for `ogr2ogr` or `COPY` loading into PostGIS.
- **Module 4 (ULPIN & Bhu-Aadhaar Integration):** Provides verified 14-character alphanumeric identifiers mapped 1:1 with parcel geometries.
- **Module 5 (Synthetic Data Generation & Simulation):** Provides extensible Python scripts and seed parameters to scale from 5,250 parcels to 50,000+ parcels.
- **Module 6 (Vector Tiles & Web GIS Visualization):** Provides polygon and linestring layers optimized for tile generation via `pg_tileserv` or `tippecanoe`.
