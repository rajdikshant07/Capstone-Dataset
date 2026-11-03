# Land Stack: Integrated GIS-Based Digital Public Infrastructure for Land Governance

## Module 1 – Data Acquisition and Dataset Preparation
### Report 3: Geospatial Database and Data Engineering
**Project Level:** Final Year B.Tech Computer Science and Engineering Capstone  
**Lead Role:** Senior GIS Engineer, Geospatial Database Architect, Data Engineer & Python Developer  
**Status:** Completed, Verified, and 100% Reproducible  

---

## 1. Project Background

**Land Stack** is an India-wide digital public infrastructure (DPI) platform engineered to unify fragmented land-related information across government departments into an integrated geospatial database.

In modern land administration, land records are siloed across revenue offices, sub-registrar registration offices, municipal tax authorities, urban town planning directorates, financial institutions, and judicial courts. Land Stack addresses this challenge by establishing a unified cadastral data model with deterministic **Unique Land Parcel Identification Numbers (ULPIN / Bhu-Aadhaar)**.

**Module 1** establishes the geospatial and multi-departmental data foundation across three culturally and administratively distinct Indian states:
1. **Maharashtra (MH)** – Mahabhulekh system (Gat Numbers, 7/12 Saat-Baara extracts, 8A Khata, e-Ferfar).
2. **Punjab (PB)** – Punjab Land Records Society (PLRS) system (Khasra Numbers, Murabba/Kila, Jamabandi, Inteqal).
3. **Gujarat (GJ)** – AnyRoR system (Block Numbers, Village Form 7/12 & 8A, e-Dhara).

---

## 2. Directory Structure

The project is structured according to professional data engineering standards:

```text
LandStack_Module1/
│
├── README.md                                  <- Master project documentation and user guide
├── requirements.txt                            <- Python dependency specifications
├── config.py                                   <- Central configuration (seeds, paths, admin hierarchy)
├── run_all.py                                  <- One-command master orchestration pipeline
│
├── 01_Data_Acquisition/                        <- Spatial and Cadastral Vector Datasets
│   ├── Administrative_Geography/               <- State, District, and Village boundaries
│   │   ├── states.geojson / states.csv
│   │   ├── districts.geojson / districts.csv
│   │   └── villages.geojson / villages.csv
│   │
│   ├── Parcel_Data/                            <- Core Cadastral Parcels (5,250 Polygons)
│   │   ├── parcels.geojson                     <- Complete GeoJSON polygon geometries & attributes
│   │   ├── parcels.csv                         <- Full CSV including WKT representations
│   │   ├── parcel_attributes.csv               <- Tabular attribute table for high-performance querying
│   │   └── parcel_geometry_metadata.csv        <- Topological metadata (vertices, bounding box, validity)
│   │
│   ├── Land_Use/                               <- Land Use & Land Cover (LULC) Classification
│   │   ├── land_use.geojson / land_use.csv
│   │   └── land_use_metadata.json
│   │
│   ├── Roads/                                  <- Synthetic Road Network (Highways, MDR, Village Roads)
│   │   ├── roads.geojson / roads.csv
│   │
│   ├── Water_Bodies/                           <- Hydrological Layer (Rivers, Canals, Tanks, Ponds)
│   │   ├── water_bodies.geojson / water_bodies.csv
│   │
│   ├── Utilities/                              <- Utility Infrastructure (Power, Water, Telecom)
│   │   ├── utilities.geojson / utilities.csv
│   │
│   ├── Survey_Records/                         <- Cadastral Survey & Khasra Registers
│   │   ├── survey_numbers.csv
│   │   └── state_survey_config.json
│   │
│   └── Source_Documentation/                   <- Provenance Registers & External Data Catalog
│       ├── dataset_source_log.csv / .xlsx
│       └── public_data_sources_reference.md
│
├── 02_Synthetic_Departmental_Records/          <- Relational Registers Linked by Parcel ID & ULPIN
│   ├── Ownership/ownership_records.csv         <- Sole, Joint, Corporate, Government, Trust titles
│   ├── RoR/ror_records.csv                     <- 7/12, Jamabandi, and VF-7/12 extracts
│   ├── Registration/property_registration.csv  <- Sub-Registrar registered deed transactions
│   ├── Property_Tax/property_tax.csv           <- Annual property tax assessments (FY 23-24 & 24-25)
│   ├── Mortgages/mortgages_encumbrances.csv    <- Bank mortgage liens and charge registrations
│   ├── Building_Permits/building_permits.csv   <- Town planning development sanctions
│   ├── Land_Restrictions/                      <- Statutory encumbrances & injunctions
│   │   ├── land_restrictions.csv
│   │   └── land_restrictions.geojson
│   └── Audit_History/audit_history.csv         <- Immutable system mutation and audit events
│
├── 03_ULPIN_Simulation/                        <- Bhu-Aadhaar Simulation Engine
│   ├── ulpin_records.csv                       <- 5,250 unique simulated 14-char ULPINs
│   ├── ulpin_generator.py                      <- Standalone Base36 deterministic generator
│   └── ulpin_validation_report.json            <- Collision and format validation report
│
├── 04_State_Mapping_Template/                  <- Cross-State Extensibility Engine
│   ├── state_mapping_template.xlsx / .csv      <- Cross-state tabular field mappings
│   ├── field_mapping_rules.json                <- Declarative transformation and regex rules
│   └── state_schema_variations.md              <- Comparative state tenure guide & plugin architecture
│
├── 05_Dataset_Inventory/                       <- Master Inventories & Data Dictionary
│   ├── module1_dataset_inventory.xlsx          <- Complete 21-sheet master inventory workbook
│   ├── data_dictionary.csv                     <- Detailed column-level data dictionary
│   └── file_inventory.csv                      <- Catalog of all 67 files in the package
│
├── 06_Initial_Data_Exploration/                <- Exploratory Data Analysis & Visualizations
│   ├── initial_data_exploration.py             <- Profiling and chart generation script
│   ├── dataset_summary.json                    <- Statistical summary metrics
│   ├── initial_exploration_report.xlsx         <- Tabular exploration report
│   ├── data_exploration_report.md              <- Comprehensive analytical findings
│   └── charts/                                 <- High-resolution (300 DPI) publication charts
│       ├── parcels_by_state.png
│       ├── parcels_by_district.png
│       ├── land_use_distribution.png
│       ├── parcel_area_distribution.png
│       ├── ownership_distribution.png
│       └── departmental_records_distribution.png
│
├── 07_Data_Quality/                            <- Automated Quality Assurance & Verification
│   ├── data_quality_checks.py                  <- Topology and referential integrity validator
│   ├── data_quality_report.json                <- Machine-readable validation report
│   ├── data_quality_report.xlsx                <- Executive QA workbook
│   └── validation_errors.csv                   <- Error register (0 errors / 100.0% Pass)
│
├── 08_Generation_Scripts/                      <- Modular Python Generation Pipeline
│   ├── individual_generation_scripts/          <- Step-by-step modular generators (01 to 20)
│   └── logs/generation_pipeline.log            <- Execution timestamp and benchmark log
│
└── docs/                                       <- Formal Engineering Documentation
    ├── Module1_Technical_Documentation.md      <- Full technical architecture and methods
    ├── Dataset_Data_Dictionary.md              <- Comprehensive field-level definitions
    ├── Dataset_Provenance_Report.md            <- Ethical provenance and authenticity declarations
    └── Module1_Completion_Report.md            <- Milestone completion and verification sign-off
```

---

## 3. Quantitative Summary of Generated Datasets

| Dataset Layer | Record Count | File Formats | Relational Key Linkage |
|---|---|---|---|
| **Cadastral Land Parcels** | **5,250** | GeoJSON, CSV | `parcel_id`, `simulated_ulpin` |
| **Simulated 14-char ULPINs** | **5,250** | CSV, JSON | 1:1 with `parcel_id` (0 Collisions) |
| **Land Use & Land Cover** | **5,250** | GeoJSON, CSV | `parcel_id`, `simulated_ulpin` |
| **Administrative Geography** | **93** (3 States, 15 Dist, 75 Vil) | GeoJSON, CSV | Administrative Hierarchy |
| **Road Network Infrastructure** | **375** | GeoJSON, CSV | `district_id`, `village_id` |
| **Hydrological Water Bodies** | **105** | GeoJSON, CSV | `district_id`, `village_id` |
| **Utility Infrastructure Assets** | **900** | GeoJSON, CSV | `parcel_id`, `village_id` |
| **Ownership Title Registry** | **6,748** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Record of Rights (RoR Extracts)** | **5,250** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Property Registration Deeds** | **2,500** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Property Tax Assessments** | **10,500** (FY 23-24 & 24-25) | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Bank Mortgages & Encumbrances** | **1,250** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Building Permits & Sanctions** | **950** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Land Restrictions & Injunctions** | **450** | GeoJSON, CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Immutable Audit Trail Events** | **3,500** | CSV | FK: `parcel_id`, `simulated_ulpin` |
| **Total Cross-Departmental Records** | **48,371** | **All Relations Verified (100% Referential Integrity)** |

---

## 4. Installation and Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Standard Python virtual environment or conda environment

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
*Required core packages:* `pandas`, `geopandas`, `shapely`, `numpy`, `pyproj`, `openpyxl`, `matplotlib`, `faker`, `pyogrio`.

---

## 5. How to Run the Pipeline

The entire generation pipeline is automated. You can regenerate the entire dataset package, run exploratory data analysis, generate charts, and execute quality assurance checks with a single command:

```bash
python run_all.py
```

Execution benchmark: Completes in **~15 seconds** on a standard modern PC. Logs are automatically written to `08_Generation_Scripts/logs/generation_pipeline.log`.

---

## 6. How to Inspect the Generated Datasets

### A. Opening Spatial GeoJSON Layers in QGIS
1. Launch **QGIS** (version 3.22+ recommended).
2. Click **Layer** -> **Add Layer** -> **Add Vector Layer...** (or drag-and-drop directly into the map canvas).
3. Navigate to `01_Data_Acquisition/Parcel_Data/parcels.geojson`.
4. Add supporting layers:
   - `01_Data_Acquisition/Roads/roads.geojson`
   - `01_Data_Acquisition/Water_Bodies/water_bodies.geojson`
   - `01_Data_Acquisition/Utilities/utilities.geojson`
   - `02_Synthetic_Departmental_Records/Land_Restrictions/land_restrictions.geojson`
5. Style parcels by categorized symbology:
   - Right-click layer -> **Properties** -> **Symbology**.
   - Select **Categorized** by `land_use_category` to view the cadastral mosaic.

### B. Checking CSV and Excel Inventories
- Open `05_Dataset_Inventory/module1_dataset_inventory.xlsx` in Microsoft Excel, LibreOffice Calc, or Google Sheets to inspect the **21 dedicated inventory sheets**.
- Open `07_Data_Quality/data_quality_report.xlsx` and `validation_errors.csv` to review the automated quality verification metrics (**100.0% Pass Rate**).
- Open `06_Initial_Data_Exploration/charts/` to view publication-quality visual distribution charts.

---

## 7. How to Proceed to Module 2 (ETL & Ingestion)

1. **Verify Raw Staging:** Confirm all CSVs and GeoJSONs exist in `01_Data_Acquisition/` and `02_Synthetic_Departmental_Records/`.
2. **Review Mapping Rules:** Inspect `04_State_Mapping_Template/field_mapping_rules.json` for column transformation and unit conversion logic.
3. **Execute ETL Cleanse:** Develop Python / PySpark / dbt transformations to load staged records into staging tables.
4. **Load to PostGIS (Module 3):** Follow the projection instructions in `docs/Module1_Technical_Documentation.md` to load geometries into PostgreSQL/PostGIS.

---

## 8. Data Authenticity & Provenance Disclaimer

> **IMPORTANT STATEMENT OF SYNTHETIC NATURE:**  
> All data assets in this repository are **100% synthetic demonstration data** created for academic evaluation in a B.Tech Computer Science Engineering capstone project.
> - Parcel boundaries are algorithmically synthesized Voronoi polygons and **must never be used as legal cadastral boundary evidence**.
> - Simulated ULPINs are academic representations and **are not official Government of India Bhu-Aadhaar identifiers**.
> - All citizen names, company names, addresses, and registration deed references are **entirely fictional**.
