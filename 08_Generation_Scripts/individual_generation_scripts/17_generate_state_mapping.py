"""
generate_state_mapping.py
Generates State-Specific Data Mapping Templates and Documentation:
- 04_State_Mapping_Template/state_mapping_template.xlsx
- 04_State_Mapping_Template/state_mapping_template.csv
- 04_State_Mapping_Template/field_mapping_rules.json
- 04_State_Mapping_Template/state_schema_variations.md
"""

import sys
import os
import json
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

MAPPING_DATA = [
    # Maharashtra
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi / Saat-Baara 7/12 & 8A)",
        "source_field": "gat_kramank",
        "common_field": "survey_number",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "TRIM(UPPER(gat_kramank)) -> Standardize prefix to 'Gat No. X'",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "REGEX_MATCH('^(Gat|Survey)\\s*No\\.\\s*\\d+')",
        "remarks": "In Maharashtra, agricultural plots are commonly designated as Gat No.; city survey plots as CTS No."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi)",
        "source_field": "peta_hissa_kramank",
        "common_field": "sub_survey_number",
        "source_datatype": "VARCHAR(20)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "COALESCE(peta_hissa_kramank, '0')",
        "null_handling": "DEFAULT_ZERO",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Sub-division of a Gat number resulting from partition or mutation."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi)",
        "source_field": "gaon_census_code",
        "common_field": "village_id",
        "source_datatype": "VARCHAR(12)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "LPAD(TRIM(gaon_census_code), 6, '0') -> Map to Land Stack VIL_MH_xxx format",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "EXISTS_IN_MASTER_VILLAGES",
        "remarks": "Census 2011 / LGD 6-digit village code."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi)",
        "source_field": "khatedar_purna_naav",
        "common_field": "owner_name",
        "source_datatype": "VARCHAR(255)",
        "target_datatype": "VARCHAR(255)",
        "transformation_rule": "CLEAN_WHITESPACE(TRANSLITERATE_DEVANAGARI_TO_LATIN(khatedar_purna_naav))",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "LENGTH >= 3",
        "remarks": "Extract of Khatedar name recorded in Register 8A and 7/12 Form."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi)",
        "source_field": "kshetraphal_hektare_aar",
        "common_field": "area_sq_m",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "NUMERIC(14,2)",
        "transformation_rule": "PARSE_HECTARE_ARE(hektare, aar) -> (hektare * 10000) + (aar * 100)",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "VALUE > 0.0",
        "remarks": "Standard revenue metric: 1 Hectare = 100 Are = 10,000 sq meters."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "Mahabhulekh (e-MahaBhumi)",
        "source_field": "bhogavatdar_varg",
        "common_field": "tenure_type",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "MAP_TENURE_CODE(bhogavatdar_varg) -> 'Occupant Class I' | 'Occupant Class II'",
        "null_handling": "DEFAULT_CLASS_I",
        "validation_rule": "IN_ENUM('Class I', 'Class II', 'Govt Lessee')",
        "remarks": "Class I has unrestricted transferability; Class II requires Collector sanction."
    },
    {
        "state": "Maharashtra",
        "state_id": "MH",
        "source_system": "e-Ferfar / e-Chavdi",
        "source_field": "ferfar_nondh_kramank",
        "common_field": "audit_mutation_number",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "TRIM(ferfar_nondh_kramank)",
        "null_handling": "SET_NULL",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Mutation entry number in Village Form 6 (Ferfar Patrak)."
    },

    # Punjab
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "khasra_no",
        "common_field": "survey_number",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "STANDARDIZE_KHASRA_PATTERN(khasra_no) -> 'Khasra No. {mustatil}//{kila}'",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "REGEX_MATCH('^Khasra\\s*No\\.\\s*\\d+//\\d+')",
        "remarks": "Punjab uses Murabba (Mustatil) and Kila numbers during consolidation (Murabba-bandi)."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "kila_sub_no",
        "common_field": "sub_survey_number",
        "source_datatype": "VARCHAR(20)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "COALESCE(kila_sub_no, '0')",
        "null_handling": "DEFAULT_ZERO",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Min-Khasra or sub-part of a kila."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "hadbast_number",
        "common_field": "village_id",
        "source_datatype": "VARCHAR(15)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "MAP_HADBAST_TO_LANDSTACK_VILLAGE(hadbast_number, tehsil_code)",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "EXISTS_IN_MASTER_VILLAGES",
        "remarks": "Every revenue village (mauza) in Punjab possesses a unique Hadbast Number."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "khewat_malik_naam",
        "common_field": "owner_name",
        "source_datatype": "VARCHAR(255)",
        "target_datatype": "VARCHAR(255)",
        "transformation_rule": "CLEAN_WHITESPACE(TRANSLITERATE_GURMUKHI_TO_LATIN(khewat_malik_naam))",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "LENGTH >= 3",
        "remarks": "Owner / co-sharer recorded in the Khewat column of Jamabandi."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "rakba_kanal_marla",
        "common_field": "area_sq_m",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "NUMERIC(14,2)",
        "transformation_rule": "CONVERT_KANAL_MARLA_TO_SQ_M(kanal, marla, sarsahi) -> (kanal * 505.857) + (marla * 25.2928)",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "VALUE > 0.0",
        "remarks": "Traditional revenue measurement: 1 Karam = 66 inches (standard); 1 Acre = 8 Kanals = 160 Marlas."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "Punjab Land Records Society (PLRS Jamabandi)",
        "source_field": "kaasht_haisiyat",
        "common_field": "tenure_type",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "MAP_TENURE_CODE(kaasht_haisiyat) -> 'Khudkasht' | 'Gair-Maroosi' | 'Muzaria'",
        "null_handling": "DEFAULT_KHUDKASHT",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Distinguishes self-cultivation (khudkasht) from tenant or lessee."
    },
    {
        "state": "Punjab",
        "state_id": "PB",
        "source_system": "PLRS Inteqal Portal",
        "source_field": "inteqal_dakhil_kharij_no",
        "common_field": "audit_mutation_number",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "TRIM(inteqal_dakhil_kharij_no)",
        "null_handling": "SET_NULL",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Dakhil-Kharij (Mutation) order number approved by Tehsildar."
    },

    # Gujarat
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat - VF-7/12 & VF-8A)",
        "source_field": "survey_block_number",
        "common_field": "survey_number",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "TRIM(UPPER(survey_block_number)) -> Format as 'Block No. X' or 'Survey No. X'",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "REGEX_MATCH('^(Block|Survey)\\s*No\\.\\s*\\d+')",
        "remarks": "Gujarat re-survey creates consolidated Block Numbers replacing historical Survey Numbers."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat)",
        "source_field": "paiki_hissa_number",
        "common_field": "sub_survey_number",
        "source_datatype": "VARCHAR(20)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "COALESCE(paiki_hissa_number, 'P1')",
        "null_handling": "DEFAULT_P1",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Paiki indicates sub-parcel division."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat)",
        "source_field": "gam_census_code",
        "common_field": "village_id",
        "source_datatype": "VARCHAR(12)",
        "target_datatype": "VARCHAR(32)",
        "transformation_rule": "LPAD(TRIM(gam_census_code), 6, '0') -> Map to Land Stack VIL_GJ_xxx format",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "EXISTS_IN_MASTER_VILLAGES",
        "remarks": "Standard Gujarat Revenue Village Census / LGD code."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat)",
        "source_field": "khatedar_naam",
        "common_field": "owner_name",
        "source_datatype": "VARCHAR(255)",
        "target_datatype": "VARCHAR(255)",
        "transformation_rule": "CLEAN_WHITESPACE(TRANSLITERATE_GUJARATI_TO_LATIN(khatedar_naam))",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "LENGTH >= 3",
        "remarks": "Registered Khatedar name recorded in Village Form 8A Khata."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat)",
        "source_field": "kshetrafal_hektare_sqm",
        "common_field": "area_sq_m",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "NUMERIC(14,2)",
        "transformation_rule": "PARSE_HECTARE_SQM(hektare, sqm) -> (hektare * 10000) + sqm",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "VALUE > 0.0",
        "remarks": "Gujarat AnyRoR standardly displays area in Hectare-Sq.Meter (Ha-Sq.m)."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "AnyRoR (Revenue Department, Gujarat)",
        "source_field": "jameen_sharat_prakar",
        "common_field": "tenure_type",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "MAP_TENURE_CODE(jameen_sharat_prakar) -> 'Juni Sharat (Old Tenure)' | 'Navi Sharat (New Tenure)'",
        "null_handling": "DEFAULT_JUNI_SHARAT",
        "validation_rule": "IN_ENUM('Juni Sharat', 'Navi Sharat', 'Sarkari')",
        "remarks": "Navi Sharat (New Tenure) requires District Collector permission for sale/mortgage."
    },
    {
        "state": "Gujarat",
        "state_id": "GJ",
        "source_system": "e-Dhara RoR Portal",
        "source_field": "nondh_kramank",
        "common_field": "audit_mutation_number",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "TRIM(nondh_kramank)",
        "null_handling": "SET_NULL",
        "validation_rule": "ALPHANUMERIC",
        "remarks": "Mutation entry number in Village Form 6 (Hakk Patrak)."
    },

    # Fourth State Plugin Architecture Template (e.g. Karnataka Bhoomi Demonstration)
    {
        "state": "Karnataka (Extensibility Template)",
        "state_id": "KA",
        "source_system": "Bhoomi (Revenue Department, Karnataka - RTC / Pahani)",
        "source_field": "survey_hissa_no",
        "common_field": "survey_number",
        "source_datatype": "VARCHAR(50)",
        "target_datatype": "VARCHAR(64)",
        "transformation_rule": "PARSE_BHOOMI_SURVEY(survey_no) -> 'Survey No. {survey_no}'",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "REGEX_MATCH('^Survey\\s*No\\.\\s*\\d+')",
        "remarks": "Demonstration template showing how Bhoomi RTC maps seamlessly into Land Stack common schema."
    },
    {
        "state": "Karnataka (Extensibility Template)",
        "state_id": "KA",
        "source_system": "Bhoomi (Revenue Department, Karnataka)",
        "source_field": "visteerna_acre_gunta",
        "common_field": "area_sq_m",
        "source_datatype": "VARCHAR(30)",
        "target_datatype": "NUMERIC(14,2)",
        "transformation_rule": "CONVERT_ACRE_GUNTA_TO_SQ_M(acre, gunta, aane) -> (acre * 4046.86) + (gunta * 101.17)",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "VALUE > 0.0",
        "remarks": "Traditional metric: 1 Acre = 40 Guntas; 1 Gunta = 1089 sq ft = 101.17 sq meters."
    },
    {
        "state": "Karnataka (Extensibility Template)",
        "state_id": "KA",
        "source_system": "Bhoomi (Revenue Department, Karnataka)",
        "source_field": "khatedar_hesaru",
        "common_field": "owner_name",
        "source_datatype": "VARCHAR(255)",
        "target_datatype": "VARCHAR(255)",
        "transformation_rule": "CLEAN_WHITESPACE(TRANSLITERATE_KANNADA_TO_LATIN(khatedar_hesaru))",
        "null_handling": "FAIL_IF_NULL",
        "validation_rule": "LENGTH >= 3",
        "remarks": "Khatedar name in RTC Column 9."
    }
]

def generate_state_mapping_artifacts():
    print("[17/20] Generating State-Specific Schema Mapping Artifacts and Plugin Documentation...")
    
    map_dir = config.STATE_MAP_DIR
    map_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Excel Workbook
    df_map = pd.DataFrame(MAPPING_DATA)
    excel_path = map_dir / "state_mapping_template.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_map.to_excel(writer, sheet_name="State_Field_Mappings", index=False)
        
    # 2. CSV File
    csv_path = map_dir / "state_mapping_template.csv"
    df_map.to_csv(csv_path, index=False)
    
    # 3. JSON Mapping Rules (Structured for ETL Ingestion Engines)
    json_path = map_dir / "field_mapping_rules.json"
    rules_dict = {
        "schema_version": "1.0.0",
        "description": "Declarative transformation and schema normalization rules for Land Stack Multi-State Ingestion Pipeline",
        "supported_states": ["MH", "PB", "GJ"],
        "extensible_template_states": ["KA"],
        "rules": MAPPING_DATA
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rules_dict, f, indent=2)
        
    # 4. State Schema Variations Markdown Guide
    md_path = map_dir / "state_schema_variations.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("""# Land Stack: State Land-Record Schema Variations and Extensibility Architecture

## 1. Executive Summary

Land administration in India is a constitutional State subject under Entry 18 of the State List (Seventh Schedule, Constitution of India). Consequently, each state has developed distinct legal terminology, land tenure systems, administrative divisions, measurement units, and digital record formats.

**Land Stack** establishes a unified, standards-compliant Common Data Model (CDM) that decouples departmental upstream variations from downstream spatial analysis, ULPIN generation, APIs, and PostGIS storage.

---

## 2. Comparative Analysis Across Sample States

| Dimension | Maharashtra (MH) | Punjab (PB) | Gujarat (GJ) | Future State (Karnataka - Bhoomi) |
|---|---|---|---|---|
| **Portal / System** | Mahabhulekh / e-MahaBhumi | PLRS Jamabandi Portal | AnyRoR / e-Dhara | Bhoomi / Kaveri |
| **Primary Cadastral Identifier** | Gat Number / Survey Number | Khasra Number (Murabba//Kila) | Survey / Block Number | Survey Number & Hissa Number |
| **Sub-division Designation** | Peta Hissa No. / Pot Hissa | Kila Sub-number | Paiki Number | Hissa Number |
| **Village Identifier** | 6-digit Census / LGD Village Code | Hadbast Number | 6-digit Census / LGD Village Code | LGD Village Code / Hobli Code |
| **Primary Record of Rights** | 7/12 Extract (Saat-Baara) | Jamabandi Nakal | Village Form 7/12 (VF-7/12) | RTC / Pahani (Form 16) |
| **Register of Owners** | Village Form 8A (Khata Vahi) | Khewat / Khatoni Register | Village Form 8A (Khata No.) | Khata Certificate |
| **Mutation Register** | Village Form 6 (Ferfar Patrak) | Inteqal (Dakhil-Kharij) | Village Form 6 (Hakk Patrak) | Mutation Register (MR) |
| **Traditional Area Units** | Hectare - Are - Sq. Meter | Kanal - Marla - Sarsahi | Hectare - Sq. Meter | Acre - Gunta - Aane |
| **Area Conversion Metric** | 1 Are = 100 sq. m; 1 Ha = 10,000 sq. m | 1 Kanal = 505.86 sq. m; 1 Marla = 25.29 sq. m | 1 Ha = 10,000 sq. m | 1 Gunta = 101.17 sq. m; 1 Acre = 4,046.86 sq. m |
| **Tenure Classification** | Bhogavatdar Class I & II | Khudkasht, Gair-Maroosi | Juni Sharat, Navi Sharat | Inam, Sarkari, Sthirasampathu |

---

## 3. Extensibility Architecture: Adding a Fourth State

To integrate an additional state (such as Karnataka, Uttar Pradesh, or Tamil Nadu) into Land Stack:
1. **No Core Database Modifications Required**: The PostgreSQL/PostGIS physical tables (`parcels`, `ownership_records`, `ror_records`, `roads`, etc.) remain identical.
2. **Add State Entry in `field_mapping_rules.json`**: Declare source field names, data types, regular expressions, and parsing functions.
3. **Plug-in Area Conversion Function**: Implement unit conversion formulas (e.g. Bigha-Katha-Dhur for UP/Bihar, or Gunta-Acre for Karnataka/Telangana) in the ETL ingestion stage.
4. **Register SRO and Administrative Jurisdictions**: Seed the new state's districts and villages into the administrative hierarchy.
5. **Run ULPIN Deterministic Generator**: Automatically produces compliant 14-character identifiers linked to parcel centroids.

---

## 4. Illustrative Field Mapping Table

```
Common Schema (Land Stack)   <-- Standardized Ingestion Pipeline <-- Raw State Record
├── parcel_id                <-- Constructed as PRCL_{state}_{dist}_{vil}_{seq}
├── simulated_ulpin          <-- Derived via 14-char deterministic geohash
├── survey_number            <-- Mapped from Gat No. (MH) / Khasra No. (PB) / Block No. (GJ)
├── area_sq_m                <-- Normalized to SI square meters from Hectare-Are / Kanal-Marla
├── owner_name               <-- Transliterated and whitespace-cleaned
└── tenure_type              <-- Categorized into normalized rights taxonomy
```

*All mappings provided in `state_mapping_template.xlsx` and `field_mapping_rules.json` are validated for cross-state ETL readiness in Module 2.*
""")
        
    print(f"  -> Generated state mapping workbook: {excel_path}")
    print(f"  -> Generated JSON rules: {json_path}")
    print(f"  -> Generated architectural documentation: {md_path}")

if __name__ == "__main__":
    generate_state_mapping_artifacts()
