"""
Land Stack: Integrated GIS-Based Digital Public Infrastructure for Land Governance
Module 1: Data Acquisition and Dataset Preparation
Configuration File: config.py
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_ACQ_DIR = BASE_DIR / "01_Data_Acquisition"
DEPT_REC_DIR = BASE_DIR / "02_Synthetic_Departmental_Records"
ULPIN_DIR = BASE_DIR / "03_ULPIN_Simulation"
STATE_MAP_DIR = BASE_DIR / "04_State_Mapping_Template"
INVENTORY_DIR = BASE_DIR / "05_Dataset_Inventory"
EXPLORATION_DIR = BASE_DIR / "06_Initial_Data_Exploration"
QUALITY_DIR = BASE_DIR / "07_Data_Quality"
SCRIPTS_DIR = BASE_DIR / "08_Generation_Scripts"
DOCS_DIR = BASE_DIR / "docs"

# Generation Parameters
RANDOM_SEED = 42
TARGET_PARCELS_PER_VILLAGE = 70  # 75 villages * 70 = 5,250 parcels (meets > 5,000 requirement)
TOTAL_PARCELS = 5250
CRS_EPSG = 4326
CRS_NAME = "EPSG:4326 (WGS 84 - 2D Geographic Coordinate Reference System)"
PROJECTED_CRS_SUGGESTION = "EPSG:32643 (UTM Zone 43N) for Maharashtra & Gujarat; EPSG:32643/32644 for Punjab"

# State and Administrative Geography Definitions
# 3 States, 15 Districts (5 per state), 75 Villages (5 per district)
ADMIN_HIERARCHY = {
    "MH": {
        "state_id": "MH",
        "state_code": "27",
        "state_name": "Maharashtra",
        "state_abbr": "MH",
        "ref_coords": {"lat": 19.7515, "lon": 75.7139},
        "districts": {
            "MH_PUN": {
                "district_id": "MH_PUN",
                "district_code": "01",
                "district_name": "Pune",
                "headquarters": "Pune",
                "lat": 18.5204,
                "lon": 73.8567,
                "villages": [
                    {"village_id": "VIL_MH_PUN_001", "village_code": "001", "village_name": "Wagholi", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.045, "lon_offset": 0.082},
                    {"village_id": "VIL_MH_PUN_002", "village_code": "002", "village_name": "Manchar", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.120, "lon_offset": -0.050},
                    {"village_id": "VIL_MH_PUN_003", "village_code": "003", "village_name": "Hinjawadi", "village_type": "Urban", "population_cat": "High", "lat_offset": 0.070, "lon_offset": -0.110},
                    {"village_id": "VIL_MH_PUN_004", "village_code": "004", "village_name": "Shirur", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.110, "lon_offset": 0.150},
                    {"village_id": "VIL_MH_PUN_005", "village_code": "005", "village_name": "Baramati", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.150, "lon_offset": 0.120}
                ]
            },
            "MH_NAG": {
                "district_id": "MH_NAG",
                "district_code": "02",
                "district_name": "Nagpur",
                "headquarters": "Nagpur",
                "lat": 21.1458,
                "lon": 79.0882,
                "villages": [
                    {"village_id": "VIL_MH_NAG_001", "village_code": "001", "village_name": "Kalmeshwar", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.090, "lon_offset": -0.070},
                    {"village_id": "VIL_MH_NAG_002", "village_code": "002", "village_name": "Saoner", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.140, "lon_offset": 0.030},
                    {"village_id": "VIL_MH_NAG_003", "village_code": "003", "village_name": "Hingna", "village_type": "Urban", "population_cat": "High", "lat_offset": -0.060, "lon_offset": -0.050},
                    {"village_id": "VIL_MH_NAG_004", "village_code": "004", "village_name": "Kamptee", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.070, "lon_offset": 0.080},
                    {"village_id": "VIL_MH_NAG_005", "village_code": "005", "village_name": "Umred", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.110, "lon_offset": 0.090}
                ]
            },
            "MH_NSK": {
                "district_id": "MH_NSK",
                "district_code": "03",
                "district_name": "Nashik",
                "headquarters": "Nashik",
                "lat": 19.9975,
                "lon": 73.7898,
                "villages": [
                    {"village_id": "VIL_MH_NSK_001", "village_code": "001", "village_name": "Ozar", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.060, "lon_offset": 0.080},
                    {"village_id": "VIL_MH_NSK_002", "village_code": "002", "village_name": "Sinnar", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.080, "lon_offset": 0.060},
                    {"village_id": "VIL_MH_NSK_003", "village_code": "003", "village_name": "Dindori", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.120, "lon_offset": -0.040},
                    {"village_id": "VIL_MH_NSK_004", "village_code": "004", "village_name": "Niphad", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.050, "lon_offset": 0.150},
                    {"village_id": "VIL_MH_NSK_005", "village_code": "005", "village_name": "Igatpuri", "village_type": "Peri-Urban", "population_cat": "Small", "lat_offset": -0.120, "lon_offset": -0.080}
                ]
            },
            "MH_CSN": {
                "district_id": "MH_CSN",
                "district_code": "04",
                "district_name": "Chhatrapati Sambhajinagar",
                "headquarters": "Chhatrapati Sambhajinagar",
                "lat": 19.8762,
                "lon": 75.3433,
                "villages": [
                    {"village_id": "VIL_MH_CSN_001", "village_code": "001", "village_name": "Paithan", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": -0.120, "lon_offset": 0.040},
                    {"village_id": "VIL_MH_CSN_002", "village_code": "002", "village_name": "Gangapur", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.030, "lon_offset": -0.120},
                    {"village_id": "VIL_MH_CSN_003", "village_code": "003", "village_name": "Vaijapur", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.050, "lon_offset": -0.150},
                    {"village_id": "VIL_MH_CSN_004", "village_code": "004", "village_name": "Khuldabad", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.080, "lon_offset": -0.040},
                    {"village_id": "VIL_MH_CSN_005", "village_code": "005", "village_name": "Kannad", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.150, "lon_offset": -0.030}
                ]
            },
            "MH_KOL": {
                "district_id": "MH_KOL",
                "district_code": "05",
                "district_name": "Kolhapur",
                "headquarters": "Kolhapur",
                "lat": 16.7050,
                "lon": 74.2433,
                "villages": [
                    {"village_id": "VIL_MH_KOL_001", "village_code": "001", "village_name": "Panhala", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.070, "lon_offset": -0.090},
                    {"village_id": "VIL_MH_KOL_002", "village_code": "002", "village_name": "Karveer", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.020, "lon_offset": 0.040},
                    {"village_id": "VIL_MH_KOL_003", "village_code": "003", "village_name": "Hatkanangle", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.050, "lon_offset": 0.120},
                    {"village_id": "VIL_MH_KOL_004", "village_code": "004", "village_name": "Shirol", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.040, "lon_offset": 0.180},
                    {"village_id": "VIL_MH_KOL_005", "village_code": "005", "village_name": "Radhanagari", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.140, "lon_offset": -0.060}
                ]
            }
        }
    },
    "PB": {
        "state_id": "PB",
        "state_code": "03",
        "state_name": "Punjab",
        "state_abbr": "PB",
        "ref_coords": {"lat": 31.1471, "lon": 75.3412},
        "districts": {
            "PB_ASR": {
                "district_id": "PB_ASR",
                "district_code": "01",
                "district_name": "Amritsar",
                "headquarters": "Amritsar",
                "lat": 31.6340,
                "lon": 74.8723,
                "villages": [
                    {"village_id": "VIL_PB_ASR_001", "village_code": "001", "village_name": "Ajnala", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.150, "lon_offset": -0.050},
                    {"village_id": "VIL_PB_ASR_002", "village_code": "002", "village_name": "Majitha", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.080, "lon_offset": 0.060},
                    {"village_id": "VIL_PB_ASR_003", "village_code": "003", "village_name": "Attari", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.040, "lon_offset": -0.140},
                    {"village_id": "VIL_PB_ASR_004", "village_code": "004", "village_name": "Jandiala Guru", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.050, "lon_offset": 0.080},
                    {"village_id": "VIL_PB_ASR_005", "village_code": "005", "village_name": "Rayya", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.080, "lon_offset": 0.140}
                ]
            },
            "PB_LDH": {
                "district_id": "PB_LDH",
                "district_code": "02",
                "district_name": "Ludhiana",
                "headquarters": "Ludhiana",
                "lat": 30.9010,
                "lon": 75.8573,
                "villages": [
                    {"village_id": "VIL_PB_LDH_001", "village_code": "001", "village_name": "Khanna", "village_type": "Urban", "population_cat": "High", "lat_offset": -0.080, "lon_offset": 0.180},
                    {"village_id": "VIL_PB_LDH_002", "village_code": "002", "village_name": "Jagraon", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.040, "lon_offset": -0.150},
                    {"village_id": "VIL_PB_LDH_003", "village_code": "003", "village_name": "Samrala", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.040, "lon_offset": 0.140},
                    {"village_id": "VIL_PB_LDH_004", "village_code": "004", "village_name": "Raikot", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.140, "lon_offset": -0.080},
                    {"village_id": "VIL_PB_LDH_005", "village_code": "005", "village_name": "Payal", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.120, "lon_offset": 0.070}
                ]
            },
            "PB_JAL": {
                "district_id": "PB_JAL",
                "district_code": "03",
                "district_name": "Jalandhar",
                "headquarters": "Jalandhar",
                "lat": 31.3260,
                "lon": 75.5762,
                "villages": [
                    {"village_id": "VIL_PB_JAL_001", "village_code": "001", "village_name": "Nakodar", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.120, "lon_offset": -0.060},
                    {"village_id": "VIL_PB_JAL_002", "village_code": "002", "village_name": "Phillaur", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.160, "lon_offset": 0.090},
                    {"village_id": "VIL_PB_JAL_003", "village_code": "003", "village_name": "Shahkot", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.100, "lon_offset": -0.140},
                    {"village_id": "VIL_PB_JAL_004", "village_code": "004", "village_name": "Goraya", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": -0.140, "lon_offset": 0.040},
                    {"village_id": "VIL_PB_JAL_005", "village_code": "005", "village_name": "Kartarpur", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.070, "lon_offset": -0.080}
                ]
            },
            "PB_PTA": {
                "district_id": "PB_PTA",
                "district_code": "04",
                "district_name": "Patiala",
                "headquarters": "Patiala",
                "lat": 30.3398,
                "lon": 76.3869,
                "villages": [
                    {"village_id": "VIL_PB_PTA_001", "village_code": "001", "village_name": "Nabha", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.030, "lon_offset": -0.150},
                    {"village_id": "VIL_PB_PTA_002", "village_code": "002", "village_name": "Rajpura", "village_type": "Urban", "population_cat": "High", "lat_offset": 0.120, "lon_offset": 0.140},
                    {"village_id": "VIL_PB_PTA_003", "village_code": "003", "village_name": "Samana", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.120, "lon_offset": -0.090},
                    {"village_id": "VIL_PB_PTA_004", "village_code": "004", "village_name": "Sanaur", "village_type": "Peri-Urban", "population_cat": "Small", "lat_offset": -0.040, "lon_offset": 0.060},
                    {"village_id": "VIL_PB_PTA_005", "village_code": "005", "village_name": "Devigarh", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.100, "lon_offset": 0.090}
                ]
            },
            "PB_BTI": {
                "district_id": "PB_BTI",
                "district_code": "05",
                "district_name": "Bathinda",
                "headquarters": "Bathinda",
                "lat": 30.2110,
                "lon": 74.9455,
                "villages": [
                    {"village_id": "VIL_PB_BTI_001", "village_code": "001", "village_name": "Talwandi Sabo", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": -0.120, "lon_offset": 0.120},
                    {"village_id": "VIL_PB_BTI_002", "village_code": "002", "village_name": "Rampura Phul", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.100, "lon_offset": 0.150},
                    {"village_id": "VIL_PB_BTI_003", "village_code": "003", "village_name": "Maur", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.060, "lon_offset": 0.140},
                    {"village_id": "VIL_PB_BTI_004", "village_code": "004", "village_name": "Goniana", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.090, "lon_offset": -0.060},
                    {"village_id": "VIL_PB_BTI_005", "village_code": "005", "village_name": "Sangat", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.110, "lon_offset": -0.080}
                ]
            }
        }
    },
    "GJ": {
        "state_id": "GJ",
        "state_code": "24",
        "state_name": "Gujarat",
        "state_abbr": "GJ",
        "ref_coords": {"lat": 22.2587, "lon": 71.1924},
        "districts": {
            "GJ_AMD": {
                "district_id": "GJ_AMD",
                "district_code": "01",
                "district_name": "Ahmedabad",
                "headquarters": "Ahmedabad",
                "lat": 23.0225,
                "lon": 72.5714,
                "villages": [
                    {"village_id": "VIL_GJ_AMD_001", "village_code": "001", "village_name": "Sanand", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.030, "lon_offset": -0.140},
                    {"village_id": "VIL_GJ_AMD_002", "village_code": "002", "village_name": "Dholka", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.150, "lon_offset": -0.060},
                    {"village_id": "VIL_GJ_AMD_003", "village_code": "003", "village_name": "Viramgam", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.120, "lon_offset": -0.220},
                    {"village_id": "VIL_GJ_AMD_004", "village_code": "004", "village_name": "Bavla", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": -0.100, "lon_offset": -0.110},
                    {"village_id": "VIL_GJ_AMD_005", "village_code": "005", "village_name": "Daskroi", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": 0.050, "lon_offset": 0.060}
                ]
            },
            "GJ_SRT": {
                "district_id": "GJ_SRT",
                "district_code": "02",
                "district_name": "Surat",
                "headquarters": "Surat",
                "lat": 21.1702,
                "lon": 72.8311,
                "villages": [
                    {"village_id": "VIL_GJ_SRT_001", "village_code": "001", "village_name": "Olpad", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.110, "lon_offset": -0.070},
                    {"village_id": "VIL_GJ_SRT_002", "village_code": "002", "village_name": "Kamrej", "village_type": "Urban", "population_cat": "High", "lat_offset": 0.060, "lon_offset": 0.080},
                    {"village_id": "VIL_GJ_SRT_003", "village_code": "003", "village_name": "Bardoli", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.050, "lon_offset": 0.160},
                    {"village_id": "VIL_GJ_SRT_004", "village_code": "004", "village_name": "Mandvi", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.100, "lon_offset": 0.200},
                    {"village_id": "VIL_GJ_SRT_005", "village_code": "005", "village_name": "Mangrol", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.170, "lon_offset": 0.110}
                ]
            },
            "GJ_BRD": {
                "district_id": "GJ_BRD",
                "district_code": "03",
                "district_name": "Vadodara",
                "headquarters": "Vadodara",
                "lat": 22.3072,
                "lon": 73.1812,
                "villages": [
                    {"village_id": "VIL_GJ_BRD_001", "village_code": "001", "village_name": "Dabhoi", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": -0.090, "lon_offset": 0.140},
                    {"village_id": "VIL_GJ_BRD_002", "village_code": "002", "village_name": "Waghodia", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.040, "lon_offset": 0.120},
                    {"village_id": "VIL_GJ_BRD_003", "village_code": "003", "village_name": "Padra", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.060, "lon_offset": -0.100},
                    {"village_id": "VIL_GJ_BRD_004", "village_code": "004", "village_name": "Karjan", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.140, "lon_offset": 0.030},
                    {"village_id": "VIL_GJ_BRD_005", "village_code": "005", "village_name": "Savli", "village_type": "Rural", "population_cat": "Small", "lat_offset": 0.130, "lon_offset": 0.050}
                ]
            },
            "GJ_RJT": {
                "district_id": "GJ_RJT",
                "district_code": "04",
                "district_name": "Rajkot",
                "headquarters": "Rajkot",
                "lat": 22.3039,
                "lon": 70.8022,
                "villages": [
                    {"village_id": "VIL_GJ_RJT_001", "village_code": "001", "village_name": "Gondal", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.140, "lon_offset": 0.000},
                    {"village_id": "VIL_GJ_RJT_002", "village_code": "002", "village_name": "Jetpur", "village_type": "Peri-Urban", "population_cat": "High", "lat_offset": -0.220, "lon_offset": -0.050},
                    {"village_id": "VIL_GJ_RJT_003", "village_code": "003", "village_name": "Jasdan", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.030, "lon_offset": 0.220},
                    {"village_id": "VIL_GJ_RJT_004", "village_code": "004", "village_name": "Dhoraji", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.250, "lon_offset": -0.180},
                    {"village_id": "VIL_GJ_RJT_005", "village_code": "005", "village_name": "Kotda Sangani", "village_type": "Rural", "population_cat": "Small", "lat_offset": -0.080, "lon_offset": 0.070}
                ]
            },
            "GJ_GND": {
                "district_id": "GJ_GND",
                "district_code": "05",
                "district_name": "Gandhinagar",
                "headquarters": "Gandhinagar",
                "lat": 23.2156,
                "lon": 72.6369,
                "villages": [
                    {"village_id": "VIL_GJ_GND_001", "village_code": "001", "village_name": "Kalol", "village_type": "Urban", "population_cat": "High", "lat_offset": 0.030, "lon_offset": -0.130},
                    {"village_id": "VIL_GJ_GND_002", "village_code": "002", "village_name": "Dehgam", "village_type": "Rural", "population_cat": "Medium", "lat_offset": -0.040, "lon_offset": 0.160},
                    {"village_id": "VIL_GJ_GND_003", "village_code": "003", "village_name": "Mansa", "village_type": "Rural", "population_cat": "Medium", "lat_offset": 0.160, "lon_offset": -0.040},
                    {"village_id": "VIL_GJ_GND_004", "village_code": "004", "village_name": "Chiloda", "village_type": "Peri-Urban", "population_cat": "Small", "lat_offset": 0.050, "lon_offset": 0.080},
                    {"village_id": "VIL_GJ_GND_005", "village_code": "005", "village_name": "Pethapur", "village_type": "Peri-Urban", "population_cat": "Medium", "lat_offset": 0.040, "lon_offset": -0.030}
                ]
            }
        }
    }
}

# Land Use Categories and Subcategories
LAND_USE_DISTRIBUTION = [
    {"category": "Agricultural", "subcategory": "Cropland Irrigated", "weight": 42},
    {"category": "Agricultural", "subcategory": "Cropland Rainfed", "weight": 18},
    {"category": "Residential", "subcategory": "Individual Detached Housing", "weight": 12},
    {"category": "Residential", "subcategory": "High Density Abadi Settlement", "weight": 8},
    {"category": "Commercial", "subcategory": "Retail and Commercial Complex", "weight": 4},
    {"category": "Industrial", "subcategory": "Light Manufacturing & Warehousing", "weight": 4},
    {"category": "Government", "subcategory": "Public Administration & Institutional", "weight": 3},
    {"category": "Forest", "subcategory": "Protected Scrub and Deciduous Cover", "weight": 4},
    {"category": "Mixed Use", "subcategory": "Commercial-cum-Residential", "weight": 3},
    {"category": "Vacant Land", "subcategory": "Fallow and Open Land", "weight": 2},
]

# Survey Number Formats per state
SURVEY_CONFIG = {
    "MH": {
        "term": "Gat / Survey Number",
        "primary_format": "Gat No. {num}",
        "sub_format": "{sub}",
        "ror_document": "7/12 Extract (Saat Baara)",
        "tax_term": "Akarani / Assessment"
    },
    "PB": {
        "term": "Khasra Number",
        "primary_format": "Khasra No. {num}",
        "sub_format": "{mustatil}//{kila}",
        "ror_document": "Jamabandi Nakal",
        "tax_term": "Chullah Tax / Municipal House Tax"
    },
    "GJ": {
        "term": "Survey / Block Number",
        "primary_format": "Block No. {num}",
        "sub_format": "P{sub}",
        "ror_document": "Village Form 7/12 (VF-7/12)",
        "tax_term": "Jameen Mehsul / Land Revenue"
    }
}

DATA_STATUS = {
    "SYNTHETIC": "SYNTHETIC",
    "REFERENCE": "REFERENCE",
    "NOT_OFFICIAL": "NOT_OFFICIAL",
    "SIMULATED": "SIMULATED"
}
