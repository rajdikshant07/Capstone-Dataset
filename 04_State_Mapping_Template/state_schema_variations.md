# Land Stack: State Land-Record Schema Variations and Extensibility Architecture

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
