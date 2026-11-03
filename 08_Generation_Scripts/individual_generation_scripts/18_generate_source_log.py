"""
18_generate_source_log.py
Generates Dataset Acquisition and Provenance Documentation:
- 01_Data_Acquisition/Source_Documentation/dataset_source_log.xlsx
- 01_Data_Acquisition/Source_Documentation/dataset_source_log.csv
- 01_Data_Acquisition/Source_Documentation/public_data_sources_reference.md
"""

import sys
import os
import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

SOURCE_LOG_ENTRIES = [
    {
        "dataset_id": "DS_ACQ_001",
        "dataset_name": "Administrative Geography - State Boundaries",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "Maharashtra, Punjab, Gujarat",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data; no government rights asserted",
        "dataset_size_approx": "15 KB",
        "original_filename": "states.geojson",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack B.Tech Capstone Project Data Engineering Pipeline",
        "notes": "Synthetic boundary envelopes created for multi-state spatial query demonstration."
    },
    {
        "dataset_id": "DS_ACQ_002",
        "dataset_name": "Administrative Geography - District Boundaries & HQs",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "15 Districts (5 MH, 5 PB, 5 GJ)",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data; no government rights asserted",
        "dataset_size_approx": "35 KB",
        "original_filename": "districts.geojson",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Synthetic district bounding envelopes and headquarters geographic anchors."
    },
    {
        "dataset_id": "DS_ACQ_003",
        "dataset_name": "Administrative Geography - Revenue Village Zones",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "75 Villages across 15 Districts",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data; no government rights asserted",
        "dataset_size_approx": "120 KB",
        "original_filename": "villages.geojson",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Synthetic cadastral perimeter zones for village-level spatial grouping."
    },
    {
        "dataset_id": "DS_ACQ_004",
        "dataset_name": "Cadastral Land Parcels (Polygon Boundaries & Attributes)",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "5,250 Parcels across 75 Villages",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data; not authoritative cadastral maps",
        "dataset_size_approx": "5.2 MB",
        "original_filename": "parcels.geojson / parcels.csv",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Seamless clipped Voronoi parcel geometries with geodesic area and perimeter."
    },
    {
        "dataset_id": "DS_ACQ_005",
        "dataset_name": "Survey Number & Khasra Records",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "5,250 Parcels in MH, PB, GJ",
        "file_format": "CSV, JSON",
        "coordinate_reference_system": "Non-spatial Tabular Register",
        "licence": "Project demonstration synthetic data",
        "dataset_size_approx": "650 KB",
        "original_filename": "survey_numbers.csv",
        "processing_status": "Generated & Linked",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Simulated state-specific survey numbering conventions (Gat No., Khasra No., Block No.)."
    },
    {
        "dataset_id": "DS_ACQ_006",
        "dataset_name": "Simulated ULPIN (Unique Land Parcel Identification Number)",
        "publisher_source": "Land Stack ULPIN Generator Engine",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "5,250 Parcels in MH, PB, GJ",
        "file_format": "CSV, JSON",
        "coordinate_reference_system": "Linked to WGS84 Centroids",
        "licence": "Simulated 14-char alphanumeric identifier for demonstration; not official GoI Bhu-Aadhaar",
        "dataset_size_approx": "550 KB",
        "original_filename": "ulpin_records.csv",
        "processing_status": "Generated & 100% Collision-Checked",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Deterministic Base36 coordinate hash; 0 collisions verified."
    },
    {
        "dataset_id": "DS_ACQ_007",
        "dataset_name": "Land Use and Land Cover (LULC)",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "5,250 Parcels in MH, PB, GJ",
        "file_format": "GeoJSON, CSV, JSON",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data",
        "dataset_size_approx": "5.3 MB",
        "original_filename": "land_use.geojson / land_use.csv",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Simulated multi-spectral satellite zonal classification into 8 standard classes."
    },
    {
        "dataset_id": "DS_ACQ_008",
        "dataset_name": "Road Network Infrastructure",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "Highways, District Roads, Village Access Roads",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data",
        "dataset_size_approx": "280 KB",
        "original_filename": "roads.geojson / roads.csv",
        "processing_status": "Generated & Connected",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Centerline vector alignments for routing and spatial buffering."
    },
    {
        "dataset_id": "DS_ACQ_009",
        "dataset_name": "Hydrological Features (Water Bodies)",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "Rivers, Canals, Lakes, Tanks, Reservoirs",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data",
        "dataset_size_approx": "210 KB",
        "original_filename": "water_bodies.geojson / water_bodies.csv",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Polygons and lines representing perennial and seasonal water bodies."
    },
    {
        "dataset_id": "DS_ACQ_010",
        "dataset_name": "Utility Infrastructure (Power, Water, Drainage, Telecom)",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "Village Utility Corridors and Point Assets",
        "file_format": "GeoJSON, CSV",
        "coordinate_reference_system": config.CRS_NAME,
        "licence": "Project demonstration synthetic data",
        "dataset_size_approx": "320 KB",
        "original_filename": "utilities.geojson / utilities.csv",
        "processing_status": "Generated & Validated",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Points (poles, towers) and lines (power lines, water mains, drains)."
    },
    {
        "dataset_id": "DS_ACQ_011",
        "dataset_name": "Departmental Land Records (Ownership, RoR, Tax, Deeds, Mortgages, Permits, Restrictions, Audit)",
        "publisher_source": "Land Stack Synthetic Data Generator",
        "source_url": "Not Applicable",
        "download_or_generation_date": datetime.date.today().isoformat(),
        "geographic_coverage": "Multi-Departmental Records linked by ULPIN / Parcel ID",
        "file_format": "CSV, GeoJSON",
        "coordinate_reference_system": "Linked to Cadastral Geometry",
        "licence": "Project demonstration synthetic data; all person and company names are entirely fictional",
        "dataset_size_approx": "4.5 MB",
        "original_filename": "8 Departmental CSVs + Restrictions GeoJSON",
        "processing_status": "Generated & Foreign-Key Linked",
        "data_origin": "Synthetic",
        "attribution": "Land Stack Project Pipeline",
        "notes": "Demonstrates cross-departmental integration without data silos."
    }
]

def generate_source_documentation():
    print("[18/20] Compiling Dataset Source Register & External Data Portals Reference...")
    
    source_dir = config.DATA_ACQ_DIR / "Source_Documentation"
    source_dir.mkdir(parents=True, exist_ok=True)
    
    df_sources = pd.DataFrame(SOURCE_LOG_ENTRIES)
    
    # 1. CSV
    csv_path = source_dir / "dataset_source_log.csv"
    df_sources.to_csv(csv_path, index=False)
    
    # 2. Excel
    excel_path = source_dir / "dataset_source_log.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_sources.to_excel(writer, sheet_name="Dataset_Source_Log", index=False)
        
    # 3. Public Data Sources Reference Markdown
    md_path = source_dir / "public_data_sources_reference.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("""# Public Geospatial and Land Record Portals Reference

> **IMPORTANT DISCLAIMER**
> The datasets packaged in Land Stack Module 1 are **100% synthetic demonstration data** generated programmatically for academic research and software engineering evaluation. None of the files in this release were downloaded from official servers, and no legally binding status or official government endorsement is implied.
>
> The real-world portals cataloged below represent authoritative government repositories that can be evaluated during future research phases (Modules 2–6) for pilot integrations subject to official data-sharing agreements and Open Data licenses.

---

## 1. National Geospatial & Mapping Portals

### 1. Survey of India (SOI)
- **Portal URL**: [https://surveyofindia.gov.in](https://surveyofindia.gov.in) / [https://onlinemaps.surveyofindia.gov.in](https://onlinemaps.surveyofindia.gov.in)
- **Role**: National Mapping Agency of India.
- **Relevant Datasets**: Open Series Maps (OSM) 1:50,000 topo sheets, Continuously Operating Reference Stations (CORS) network data, National Topographic Database.
- **Access Model**: Free registration for PDF sheets; DGPS / CORS positioning feeds via subscription; High-resolution digital vectors restricted.

### 2. ISRO Bhuvan (National Geospatial Portal)
- **Portal URL**: [https://bhuvan.nrsc.gov.in](https://bhuvan.nrsc.gov.in)
- **Role**: Indian Space Research Organisation (NRSC) geospatial platform.
- **Relevant Datasets**: LULC (1:50k and 1:250k), Geomorphology, Watershed Boundaries, Cartosat DEMs, Bhuvan Thematic WMS/WFS services.
- **Access Model**: Open WMS viewing; vector downloads available for selected thematic layers upon scientific institutional registration.

### 3. Open Government Data (OGD) Platform India (data.gov.in)
- **Portal URL**: [https://data.gov.in](https://data.gov.in)
- **Role**: National open data portal under National Data Sharing and Accessibility Policy (NDSAP).
- **Relevant Datasets**: Administrative boundaries (state, district, taluk, village points), Census LGD codes, soil classifications, rainfall statistics.
- **Access Model**: Open API / CSV / JSON downloads under National Open Data License.

### 4. NAKSHA (Survey of India Web GIS)
- **Portal URL**: [https://naksha.gov.in](https://naksha.gov.in)
- **Role**: Web GIS portal providing SOI topographic sheets and baseline geographic layers.
- **Access Model**: Public web GIS viewer; restricted download privileges.

---

## 2. Rural Land Records & Cadastral Modernization

### 5. DILRMP (Digital India Land Records Modernization Programme)
- **Portal URL**: [https://dilrmp.gov.in](https://dilrmp.gov.in)
- **Administering Ministry**: Department of Land Resources (DoLR), Ministry of Rural Development, Govt. of India.
- **Relevant Systems**: Computerization of Land Records (CLR), Survey/Resurvey using modern technology (DGPS, Drone, ETS), Computerization of Registration (CoR), Modern Record Rooms (MRR).
- **ULPIN Context**: DoLR is the apex custodian of the 14-digit Unique Land Parcel Identification Number (Bhu-Aadhaar) roll-out nationwide.

### 6. SVAMITVA Scheme (Survey of Villages Abadi & Mapping with Improvised Technology in Village Areas)
- **Portal URL**: [https://svamitva.nic.in](https://svamitva.nic.in)
- **Administering Ministry**: Ministry of Panchayati Raj, Govt. of India in collaboration with Survey of India.
- **Relevance**: Drone-based large scale mapping (1:500 scale) of rural inhabited (abadi) land parcels and issuance of Property Cards (Sampatti Patrak).

---

## 3. Infrastructure & Transport Networks

### 7. GeoSadak / PMGSY Online Management, Monitoring and Accounting System (OMMAS)
- **Portal URL**: [https://geosadak-pmgsy.nic.in](https://geosadak-pmgsy.nic.in)
- **Administering Body**: National Rural Infrastructure Development Agency (NRIDA), Ministry of Rural Development.
- **Relevant Datasets**: GIS alignment of rural road networks, habitations, PMGSY core networks, bridges, and village connectivity matrices.
- **Access Model**: Web GIS visualization; data exports restricted to authorized state road development agencies.

---

## 4. State Land Records Portals

### 8. Maharashtra: Mahabhulekh / e-MahaBhumi
- **Portal URL**: [https://bhulekh.mahabhumi.gov.in](https://bhulekh.mahabhumi.gov.in)
- **Services**: Digital 7/12 (Saat-Baara) extracts, 8A Khata extracts, e-Ferfar (online mutation), e-Chavdi.
- **Cadastral Maps**: [https://mahabhunakasha.mahabhumi.gov.in](https://mahabhunakasha.mahabhumi.gov.in) (Bhunaksha vector parcel viewer).

### 9. Punjab: Punjab Land Records Society (PLRS)
- **Portal URL**: [https://plrs.org.in](https://plrs.org.in)
- **Services**: Jamabandi Nakal, Khasra Girdawari (crop inspection register), Inteqal (mutation status), Roznamcha Waqiati.
- **Cadastral Maps**: Bhunaksha integration in pilot tehsils.

### 10. Gujarat: AnyRoR Anywhere (e-Dhara)
- **Portal URL**: [https://anyror.gujarat.gov.in](https://anyror.gujarat.gov.in)
- **Services**: Village Form 7/12 (VF-7/12), Village Form 8A (Khata), Village Form 6 (Mutation), Urban Property Card verification.
- **Cadastral Maps**: [https://revenue.gujarat.gov.in](https://revenue.gujarat.gov.in) (Bhunaksha Gujarat).

---

## 5. Community & Open Data Repositories

### 11. OpenStreetMap (OSM) & Geofabrik India Extracts
- **Portal URL**: [https://download.geofabrik.de/asia/india.html](https://download.geofabrik.de/asia/india.html)
- **Relevant Datasets**: Road centerlines, water bodies, village settlement points, landuse polygons.
- **Licence**: Open Database License (ODbL).
""")
        
    print(f"  -> Generated source log CSV: {csv_path}")
    print(f"  -> Generated source log Excel: {excel_path}")
    print(f"  -> Generated public data sources reference: {md_path}")

if __name__ == "__main__":
    generate_source_documentation()
