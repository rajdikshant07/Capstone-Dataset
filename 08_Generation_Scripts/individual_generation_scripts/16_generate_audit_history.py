"""
16_generate_audit_history.py
Generates Audit and Change History trail records for traceability:
- 02_Synthetic_Departmental_Records/Audit_History/audit_history.csv
"""

import sys
import os
import json
import random
import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

AUDIT_USERS = {
    "MH": ["talathi_pune_rev04", "circle_officer_nagpur", "talathi_nashik_rural", "sys_dlr_mahabhulekh"],
    "PB": ["patwari_ldh_circle02", "kanungo_amritsar_div", "patwari_patiala_east", "sys_plrs_gateway"],
    "GJ": ["talati_sanand_gj", "cir_inspector_surat", "talati_vadodara_west", "sys_anyror_sync"]
}

OPERATIONS = [
    {
        "op": "INSERT",
        "tbl": "parcels",
        "old_val": "N/A (Initial Record Creation)",
        "new_val": "{'status': 'Active', 'cadastre_ingestion': 'Phase-I'}",
        "reason": "Initial digital cadastral boundary capture via DGPS resurvey"
    },
    {
        "op": "MUTATION_RECORDED",
        "tbl": "ownership_records",
        "old_val": "{'owner': 'Previous Titleholder', 'share': 100.0}",
        "new_val": "{'owner': 'Registered Transferee', 'share': 100.0}",
        "reason": "Mutation registered following certified Sale Deed registration"
    },
    {
        "op": "UPDATE",
        "tbl": "parcels",
        "old_val": "{'land_type': 'Agricultural', 'land_use': 'Agricultural'}",
        "new_val": "{'land_type': 'Non-Agricultural', 'land_use': 'Residential'}",
        "reason": "Non-Agricultural (NA) conversion order passed by District Collector"
    },
    {
        "op": "ENCUMBRANCE_CREATED",
        "tbl": "mortgages_encumbrances",
        "old_val": "{'charge_status': 'None'}",
        "new_val": "{'bank_charge': 'Equitable Mortgage Recorded', 'status': 'Active'}",
        "reason": "Commercial bank loan lien marked on Record of Rights"
    },
    {
        "op": "TAX_ASSESSED",
        "tbl": "property_tax",
        "old_val": "{'financial_year': '2022-2023'}",
        "new_val": "{'financial_year': '2023-2024', 'revision': 'Annual Revision'}",
        "reason": "Annual statutory property tax reassessment and rate schedule update"
    },
    {
        "op": "RESTRICTION_NOTIFIED",
        "tbl": "land_restrictions",
        "old_val": "{'legal_status': 'Clear'}",
        "new_val": "{'restriction': 'Interim Injunction Order', 'status': 'Active'}",
        "reason": "Civil Court stay order communication entered into land registry"
    }
]

def generate_audit_history():
    print("[16/20] Generating Synthetic Audit & Change History Dataset...")
    random.seed(config.RANDOM_SEED)
    
    audit_dir = config.DEPT_REC_DIR / "Audit_History"
    audit_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    # Sample ~3,500 audit events
    sampled = df_parcels.sample(n=3500, random_state=config.RANDOM_SEED)
    
    audit_rows = []
    
    for idx, (_, p_row) in enumerate(sampled.iterrows(), start=1):
        p_id = p_row["parcel_id"]
        ulpin = p_row["simulated_ulpin"]
        s_id = p_row["state_id"]
        
        audit_id = f"AUD_{s_id}_{idx:07d}"
        op_info = random.choice(OPERATIONS)
        
        a_year = random.choice([2021, 2022, 2023, 2024])
        a_date = datetime.date(a_year, 1, 1) + datetime.timedelta(days=random.randint(1, 350))
        a_time = f"{random.randint(9, 18):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        timestamp_str = f"{a_date.isoformat()}T{a_time}Z"
        
        user_name = random.choice(AUDIT_USERS[s_id])
        
        audit_rows.append({
            "audit_id": audit_id,
            "parcel_id": p_id,
            "simulated_ulpin": ulpin,
            "operation_type": op_info["op"],
            "table_name": op_info["tbl"],
            "old_value": op_info["old_val"],
            "new_value": op_info["new_val"],
            "modified_by": user_name,
            "timestamp": timestamp_str,
            "change_reason": op_info["reason"],
            "data_status": config.DATA_STATUS["SYNTHETIC"],
            "provenance": "Synthetic immutable audit trail event"
        })
        
    df_audit = pd.DataFrame(audit_rows)
    csv_out = audit_dir / "audit_history.csv"
    df_audit.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_audit)} audit trail events in {csv_out}")

if __name__ == "__main__":
    generate_audit_history()
