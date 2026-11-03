# Land Stack: Dataset Provenance & Authenticity Report
## Module 1 – Data Acquisition and Dataset Preparation
**Release Version:** 1.0.0 (Synthetic Benchmark)  
**Security & Privacy Assessment:** Clean (Zero PII, Zero Proprietary Government Data)  

---

## 1. Statement of Authenticity and Provenance Principles

The **Land Stack** project is an academic computer science capstone developed to design, test, and demonstrate digital public infrastructure for integrated land governance.

In adherence to data ethics, privacy regulations, and project guidelines:
1. **100% Synthetic Datasets:** No official cadastral maps, scanned deed books, real taxpayer files, or live bank encumbrance ledgers were harvested, scraped, or acquired from government servers.
2. **Zero Personally Identifiable Information (PII):** All citizen names, corporate identities, residential addresses, deed registration IDs, and mortgage values were generated using statistical modeling and fictional name pools. Any resemblance to real individuals, living or deceased, or actual land disputes is purely coincidental.
3. **Transparent Provenance Classification:** Every dataset file, database table, and individual record contains an explicit `data_status` attribute declaring its synthetic origin.

---

## 2. Classification Taxonomy of Project Data Elements

| Provenance Classification | Definition & Usage in Land Stack | Datasets & Layers Covered |
|---|---|---|
| `REFERENCE` | Publicly known, non-confidential administrative and geographic anchors used solely to place synthetic village clusters in plausible geographic regions. | District headquarters latitudes/longitudes; State names; Census 2011 state/district LGD identification codes. |
| `SYNTHETIC` | Algorithmic data generated programmatically using mathematical models, Voronoi tessellation, and statistical distributions. | Parcel polygon geometries (`parcels.geojson`), Road alignments (`roads.geojson`), Water bodies (`water_bodies.geojson`), Utilities (`utilities.geojson`), Land use vectors (`land_use.geojson`). |
| `SIMULATED` | Identifiers and certificates designed to mirror structural specifications of planned government standards for software engineering demonstration. | Simulated 14-char ULPINs (`ulpin_records.csv`); Simulated 7/12 & Jamabandi extracts (`ror_records.csv`); State schema mapping rules (`field_mapping_rules.json`). |
| `NOT_OFFICIAL` | Administrative records synthesized to demonstrate multi-departmental relational joining without official legal standing. | Sub-Registrar deed transactions (`property_registration.csv`), Municipal tax demands (`property_tax.csv`), Bank mortgages (`mortgages_encumbrances.csv`), Town planning permits (`building_permits.csv`), Injunctions (`land_restrictions.csv`). |

---

## 3. Detailed Provenance Breakdown by Component

### 3.1 Administrative Geography
- **Origin:** District headquarters points are based on publicly known geographical coordinates of major Indian cities (e.g. Pune: 18.5204° N, 73.8567° E).
- **Synthetic Component:** Village locations are synthesized by offsetting coordinates from district centroids. State and district boundary polygons are synthetic spatial envelopes designed to test hierarchical geospatial bounding queries.

### 3.2 Cadastral Parcel Geometries
- **Origin:** Programmatically synthesized using a Clipped Voronoi Mosaic Algorithm in Shapely.
- **Cadastral Boundary Disclaimer:** These boundaries do not represent legally surveyed land boundaries. They must never be used for land boundary demarcation, physical possession, or court litigation.

### 3.3 ULPIN / Bhu-Aadhaar Simulation
- **Origin:** Synthesized via `ulpin_generator.py` using Base36 spatial coordinate hashing.
- **Specification Disclaimer:** The Government of India's official ULPIN implementation is operated by the Department of Land Resources (DoLR), NIC, and Survey of India using proprietary server keys. The Land Stack ULPIN format is an academic simulation designed to demonstrate unique identifier mapping.

### 3.4 Departmental & Financial Records
- **Ownership Titles:** Generated using weighted probabilistic distributions across individual, joint, corporate, and governmental ownership classes. Names use regionally typical Indian naming conventions drawn from public linguistic dictionaries.
- **Deeds & Stamp Duties:** Valuations and tax amounts are modeled on typical ready-reckoner rate brackets across urban, peri-urban, and agricultural zones.
- **Bank Encumbrances:** Lending institutions are labeled with fictional names (e.g., *State Apex Agriculture & Rural Development Cooperative Bank*) to prevent confusion with actual commercial banking entities.

---

## 4. Verification and Audit Traceability

All data generation scripts are committed in the repository under `08_Generation_Scripts/individual_generation_scripts/`. By running:
```bash
python run_all.py
```
with random seed `42`, any evaluator or researcher can regenerate the complete 5,250-parcel dataset package byte-for-byte, verifying that no external private datasets were injected.
