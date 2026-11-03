# Land Stack: Dataset Data Dictionary
## Module 1 – Data Acquisition and Dataset Preparation
**Standard Coordinate Reference System:** EPSG:4326 (WGS 84 2D)  
**Data Status:** 100% Synthetic Demonstration Data  

---

## 1. Cadastral Land Parcels (`parcels.geojson` / `parcels.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `parcel_id` | VARCHAR(32) | NO | YES | None | Unique synthesized cadastral parcel identifier | `PRCL_27_01_001_0001` |
| `state_id` | VARCHAR(4) | NO | NO | `states(state_id)` | Two-letter state identifier (MH, PB, GJ) | `MH` |
| `state_name` | VARCHAR(64) | NO | NO | None | Formal name of the Indian State | `Maharashtra` |
| `district_id` | VARCHAR(16) | NO | NO | `districts(district_id)` | Unique district code | `MH_PUN` |
| `district_name` | VARCHAR(64) | NO | NO | None | Name of the revenue district | `Pune` |
| `village_id` | VARCHAR(24) | NO | NO | `villages(village_id)` | Unique village code within the district | `VIL_MH_PUN_001` |
| `village_name` | VARCHAR(64) | NO | NO | None | Name of the revenue village or mauza | `Wagholi` |
| `survey_number` | VARCHAR(32) | NO | NO | None | Survey number formatted per state conventions | `Gat No. 12` |
| `sub_survey_number` | VARCHAR(16) | NO | NO | None | Sub-division, pot-hissa, or kila number | `1` |
| `parcel_number` | INTEGER | NO | NO | None | Sequential parcel number within the village | `1` |
| `land_type` | VARCHAR(32) | NO | NO | None | Broad statutory classification | `Agricultural` |
| `land_use_category`| VARCHAR(32) | NO | NO | None | Functional land use category | `Residential` |
| `area_sq_m` | NUMERIC(14,2)| NO | NO | None | True geodesic polygon area in square meters | `1425.80` |
| `area_hectares` | NUMERIC(10,4)| NO | NO | None | Geodesic area converted to hectares | `0.1426` |
| `perimeter_m` | NUMERIC(12,2)| NO | NO | None | True geodesic boundary perimeter in meters | `154.20` |
| `centroid_latitude`| NUMERIC(9,6) | NO | NO | None | Latitude of polygon centroid (WGS 84) | `18.524510` |
| `centroid_longitude`| NUMERIC(9,6)| NO | NO | None | Longitude of polygon centroid (WGS 84) | `73.861230` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | 14-char simulated parcel identifier | `2701001A8B2C4D` |
| `record_status` | VARCHAR(24) | NO | NO | None | Record lifecycle state (Active, Mutated, etc.) | `Active` |
| `created_at` | DATE | NO | NO | None | Ingestion timestamp | `2022-04-14` |
| `updated_at` | DATE | NO | NO | None | Last revision timestamp | `2024-02-18` |
| `data_status` | VARCHAR(16) | NO | NO | None | Provenance classification flag | `SYNTHETIC` |

---

## 2. Parcel Geometry Metadata (`parcel_geometry_metadata.csv`)

| Field Name | Datatype | Nullable | Primary Key | Description | Sample Value |
|---|---|---|---|---|---|
| `parcel_id` | VARCHAR(32) | NO | YES (FK) | Reference to cadastral parcel | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO (FK) | Reference to simulated ULPIN | `2701001A8B2C4D` |
| `geometry_type` | VARCHAR(24) | NO | NO | Geometric primitive type | `Polygon` |
| `num_vertices` | INTEGER | NO | NO | Total boundary coordinate vertices | `6` |
| `is_valid` | BOOLEAN | NO | NO | Shapely topological validity flag | `True` |
| `is_simple` | BOOLEAN | NO | NO | Simple geometry assertion (no self-crossings)| `True` |
| `is_closed` | BOOLEAN | NO | NO | Closed linear ring assertion | `True` |
| `bbox_min_lon` | NUMERIC(9,6) | NO | NO | Bounding box minimum longitude | `73.858200` |
| `bbox_min_lat` | NUMERIC(9,6) | NO | NO | Bounding box minimum latitude | `18.521100` |
| `bbox_max_lon` | NUMERIC(9,6) | NO | NO | Bounding box maximum longitude | `73.863400` |
| `bbox_max_lat` | NUMERIC(9,6) | NO | NO | Bounding box maximum latitude | `18.526800` |
| `geodesic_area_sq_m` | NUMERIC(14,2)| NO | NO | Ellipsoidal geodesic area | `1425.80` |
| `geodesic_perimeter_m`| NUMERIC(12,2)| NO | NO | Ellipsoidal geodesic perimeter | `154.20` |
| `crs` | VARCHAR(64) | NO | NO | Coordinate reference system | `EPSG:4326 (WGS 84)` |
| `verification_status`| VARCHAR(16) | NO | NO | QA inspection status | `VALID` |

---

## 3. Simulated ULPIN Registry (`ulpin_records.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `ulpin` | VARCHAR(14) | NO | YES | None | 14-char deterministic alphanumeric ULPIN | `2701001A8B2C4D` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `state_id` | VARCHAR(4) | NO | NO | `states(state_id)` | Two-letter state identifier | `MH` |
| `state_code` | VARCHAR(2) | NO | NO | None | 2-digit Census/LGD state code | `27` |
| `district_id` | VARCHAR(16) | NO | NO | `districts(district_id)` | District code | `MH_PUN` |
| `district_code` | VARCHAR(2) | NO | NO | None | 2-digit district sample code | `01` |
| `village_id` | VARCHAR(24) | NO | NO | `villages(village_id)` | Village code | `VIL_MH_PUN_001` |
| `village_code` | VARCHAR(3) | NO | NO | None | 3-digit village sample code | `001` |
| `centroid_latitude`| NUMERIC(9,6) | NO | NO | None | Centroid latitude coordinate | `18.524510` |
| `centroid_longitude`| NUMERIC(9,6)| NO | NO | None | Centroid longitude coordinate | `73.861230` |
| `generation_method`| VARCHAR(48) | NO | NO | None | Simulation algorithm type | `DETERMINISTIC_GEO_BASE36` |
| `generation_timestamp`| TIMESTAMP | NO | NO | None | Generation timestamp in UTC | `2026-11-03T00:10:48Z` |
| `uniqueness_status`| VARCHAR(24) | NO | NO | None | Integrity assurance flag | `GUARANTEED_UNIQUE` |
| `data_status` | VARCHAR(16) | NO | NO | None | Data provenance classification | `SIMULATED` |
| `disclaimer` | VARCHAR(255)| NO | NO | None | Statutory non-official disclaimer | `Simulation only` |

---

## 4. Ownership Registry (`ownership_records.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `owner_id` | VARCHAR(24) | NO | YES | None | Unique synthetic owner identifier | `OWN_MH_000104` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | Linked simulated ULPIN | `2701001A8B2C4D` |
| `owner_name` | VARCHAR(255)| NO | NO | None | Synthesized owner full name | `Ramesh Patil` |
| `ownership_type` | VARCHAR(24) | NO | NO | None | Type: Individual, Joint, Company, Govt, Trust | `Individual` |
| `ownership_percentage`| NUMERIC(5,2)| NO | NO | None | Titleholder share percentage | `100.00` |
| `fictional_address`| VARCHAR(255)| NO | NO | None | Generated non-personal fictional address | `Plot 42, Near Shivaji Chowk`|
| `state_id` | VARCHAR(4) | NO | NO | `states(state_id)` | State identifier | `MH` |
| `district_id` | VARCHAR(16) | NO | NO | `districts(district_id)` | District identifier | `MH_PUN` |
| `village_id` | VARCHAR(24) | NO | NO | `villages(village_id)` | Village identifier | `VIL_MH_PUN_001` |
| `acquisition_date` | DATE | NO | NO | None | Date of title acquisition | `2018-06-22` |
| `ownership_status` | VARCHAR(24) | NO | NO | None | Title status (Active, Historical, etc.) | `Active` |

---

## 5. Record of Rights (`ror_records.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `ror_id` | VARCHAR(24) | NO | YES | None | Unique Record of Rights certificate ID | `ROR_MH_000001` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | Linked simulated ULPIN | `2701001A8B2C4D` |
| `survey_number` | VARCHAR(32) | NO | NO | None | Cadastral survey reference | `Gat No. 12` |
| `sub_survey_number`| VARCHAR(16)| NO | NO | None | Sub-division reference | `1` |
| `primary_owner_id` | VARCHAR(24) | NO | NO | `ownership_records(owner_id)`| Primary Khatedar reference | `OWN_MH_000001` |
| `land_classification`| VARCHAR(48)| NO | NO | None | Revenue land class (Jirayat, Bagayat, etc.)| `Bagayat (Garden/Irrigated)` |
| `cultivation_details`| VARCHAR(64)| NO | NO | None | Crop name / seasonal cultivation | `Sugarcane (Adsali)` |
| `irrigation_status`| VARCHAR(48) | NO | NO | None | Water source classification | `Well / Borewell` |
| `tenure_type` | VARCHAR(64) | NO | NO | None | Statutory tenure rights category | `Occupant Class I` |
| `state_ror_extract_type`| VARCHAR(48)| NO | NO | None | State document form designation | `7/12 Extract (Saat-Baara)` |
| `state_specific_metadata`| VARCHAR(255)| NO | NO | None | Khata, mutation, or revenue details | `Khata No: 342, Mutation: #4120` |
| `record_year` | INTEGER | NO | NO | None | Revenue certification year | `2024` |
| `record_status` | VARCHAR(24) | NO | NO | None | Verification status | `Certified` |

---

## 6. Property Registration Deeds (`property_registration.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `registration_id` | VARCHAR(24) | NO | YES | None | Unique registered deed identifier | `REG_MH_000001` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | Linked simulated ULPIN | `2701001A8B2C4D` |
| `deed_number` | VARCHAR(32) | NO | NO | None | SRO registered deed document number | `DOC-MH-2023-4521` |
| `deed_type` | VARCHAR(32) | NO | NO | None | Deed nature: Sale, Gift, Lease, etc. | `Sale Deed` |
| `seller_owner_id` | VARCHAR(24) | NO | NO | `ownership_records(owner_id)`| Transferor owner identifier | `OWN_MH_000104` |
| `buyer_owner_id` | VARCHAR(24) | NO | NO | `ownership_records(owner_id)`| Transferee owner identifier | `OWN_MH_000215` |
| `registration_date`| DATE | NO | NO | None | Registration execution date | `2023-08-14` |
| `transaction_value_inr`| NUMERIC(14,2)| NO | NO | None | Consideration transaction value (INR) | `4500000.00` |
| `stamp_duty_inr` | NUMERIC(12,2)| NO | NO | None | Assessed statutory stamp duty (INR) | `270000.00` |
| `registration_fee_inr`| NUMERIC(10,2)| NO | NO | None | SRO registration charge (INR) | `30000.00` |
| `sub_registrar_office`| VARCHAR(64)| NO | NO | None | Fictional Sub-Registrar Office | `SRO Haveli No. 3 (Pune)` |
| `registration_status`| VARCHAR(24)| NO | NO | None | Deed lifecycle state | `Registered` |

---

## 7. Property Tax Assessments (`property_tax.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `tax_id` | VARCHAR(24) | NO | YES | None | Unique tax assessment demand ID | `TAX_MH_0000001` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | Linked simulated ULPIN | `2701001A8B2C4D` |
| `financial_year` | VARCHAR(12) | NO | NO | None | Tax assessment financial year | `2024-2025` |
| `taxable_value_inr`| NUMERIC(14,2)| NO | NO | None | Rateable annual valuation (INR) | `450000.00` |
| `tax_amount_inr` | NUMERIC(10,2)| NO | NO | None | Base annual property tax demand (INR) | `1850.00` |
| `penalty_inr` | NUMERIC(10,2)| NO | NO | None | Statutory interest or late fee (INR) | `0.00` |
| `total_payable_inr`| NUMERIC(10,2)| NO | NO | None | Net payable amount (INR) | `1850.00` |
| `payment_status` | VARCHAR(16) | NO | NO | None | Collection status: Paid, Unpaid, Overdue | `Paid` |
| `payment_date` | VARCHAR(16) | YES| NO | None | Payment receipt date (or N/A) | `2024-06-18` |
| `tax_authority` | VARCHAR(64) | NO | NO | None | Fictional collecting local body | `Gram Panchayat Wagholi` |

---

## 8. Mortgages & Encumbrances (`mortgages_encumbrances.csv`)

| Field Name | Datatype | Nullable | Primary Key | Foreign Key | Description | Sample Value |
|---|---|---|---|---|---|---|
| `encumbrance_id` | VARCHAR(24) | NO | YES | None | Unique encumbrance charge ID | `ENC_MH_000001` |
| `parcel_id` | VARCHAR(32) | NO | NO | `parcels(parcel_id)` | Linked parcel identifier | `PRCL_27_01_001_0001` |
| `simulated_ulpin` | VARCHAR(14) | NO | NO | `ulpin_records(ulpin)` | Linked simulated ULPIN | `2701001A8B2C4D` |
| `mortgage_id` | VARCHAR(32) | NO | NO | None | Financial institution loan reference | `MTG-MH-2022-45120` |
| `lender_name` | VARCHAR(128)| NO | NO | None | Fictionalized institutional creditor | `State Apex Agriculture Coop Bank`|
| `loan_amount_inr` | NUMERIC(14,2)| NO | NO | None | Sanctioned mortgage credit limit (INR) | `850000.00` |
| `mortgage_date` | DATE | NO | NO | None | Charge registration date | `2022-03-15` |
| `loan_status` | VARCHAR(24) | NO | NO | None | Credit status: Active, Closed, etc. | `Active / Servicing` |
| `release_date` | VARCHAR(16) | YES| NO | None | Lien discharge date (or N/A) | `N/A` |
| `encumbrance_status`| VARCHAR(24)| NO | NO | None | Title status: Active Encumbrance / Released| `Active Encumbrance` |

---

## 9. Infrastructure Layers (`roads.csv`, `water_bodies.csv`, `utilities.csv`)

### Roads
- `road_id` (PK): Unique road alignment code (`RD_MH_00001`).
- `road_name`: Standard descriptive corridor designation.
- `road_category`: National Highway, State Highway, District Road, Village Road, Local Road.
- `road_surface`: Bituminous (Asphalt), Concrete, WBM, Earthen.
- `road_width_m`: Carriageway plus shoulder width in meters (3.75 m – 14.0 m).
- `road_length_m`: Geodesic centerline alignment length in meters.

### Water Bodies
- `waterbody_id` (PK): Unique hydrological feature code (`WB_MH_00001`).
- `waterbody_name`: Descriptive regional or village name.
- `waterbody_type`: River, Canal, Lake, Pond, Reservoir.
- `geometry_type`: Polygon or LineString.
- `approx_area_sq_m`: Geodesic surface water area in square meters.

### Utilities
- `utility_id` (PK): Unique infrastructure asset code (`UTL_MH_000001`).
- `utility_type`: Electricity Line (11kV), Pole/Transformer, Water Main, Drain, Telecom Mast.
- `parcel_id` (FK): Underlying cadastral lot or right-of-way corridor.
- `operational_status`: Operational, Maintenance, Decommissioned.
- `capacity_spec`: Technical capacity description (e.g. 100 kVA Transformer, 200mm DI Pipe).
