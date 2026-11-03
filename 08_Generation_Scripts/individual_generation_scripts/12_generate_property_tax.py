"""
12_generate_property_tax.py
Generates Property Tax assessment and collection records across two financial years:
- 02_Synthetic_Departmental_Records/Property_Tax/property_tax.csv
"""

import sys
import os
import random
import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

import config

def generate_property_tax():
    print("[12/20] Generating Synthetic Property Tax Assessments (FY 2023-24 & 2024-25)...")
    random.seed(config.RANDOM_SEED)
    
    tax_dir = config.DEPT_REC_DIR / "Property_Tax"
    tax_dir.mkdir(parents=True, exist_ok=True)
    
    parcels_attr_path = config.DATA_ACQ_DIR / "Parcel_Data" / "parcel_attributes.csv"
    if not parcels_attr_path.exists():
        raise FileNotFoundError(f"Missing {parcels_attr_path}. Run 02_generate_parcels.py first.")
        
    df_parcels = pd.read_csv(parcels_attr_path)
    
    tax_rows = []
    tax_counter = 1
    
    financial_years = ["2023-2024", "2024-2025"]
    
    for fy in financial_years:
        is_current_fy = (fy == "2024-2025")
        
        for _, p_row in df_parcels.iterrows():
            p_id = p_row["parcel_id"]
            ulpin = p_row["simulated_ulpin"]
            s_id = p_row["state_id"]
            d_name = p_row["district_name"]
            v_name = p_row["village_name"]
            l_use = p_row["land_use_category"]
            area_m2 = p_row["area_sq_m"]
            
            tax_id = f"TAX_{s_id}_{tax_counter:07d}"
            tax_counter += 1
            
            # Taxable value and annual tax
            if l_use in ["Commercial", "Mixed Use"]:
                unit_tax = random.uniform(25.0, 65.0)
                taxable_val = area_m2 * random.uniform(8000, 25000)
            elif l_use == "Industrial":
                unit_tax = random.uniform(18.0, 45.0)
                taxable_val = area_m2 * random.uniform(4000, 12000)
            elif l_use == "Residential":
                unit_tax = random.uniform(6.0, 18.0)
                taxable_val = area_m2 * random.uniform(3000, 9000)
            else: # Agricultural, Forest, Vacant (nominal land revenue cess)
                unit_tax = random.uniform(0.15, 0.85)
                taxable_val = area_m2 * random.uniform(100, 400)
                
            base_tax = round(area_m2 * unit_tax, 2)
            base_tax = max(50.0, min(base_tax, 250000.0))
            taxable_val = round(taxable_val, 2)
            
            # Payment status and dates
            if not is_current_fy:
                # Past year: high paid rate
                status = random.choices(["Paid", "Overdue"], weights=[92, 8])[0]
            else:
                # Current year: mix of paid, unpaid, overdue
                status = random.choices(["Paid", "Unpaid", "Overdue"], weights=[68, 24, 8])[0]
                
            if status == "Paid":
                penalty = 0.0
                total_due = base_tax
                p_month = random.randint(4, 11)
                p_year = int(fy.split("-")[0])
                pay_date = f"{p_year}-{p_month:02d}-{random.randint(5, 25):02d}"
            elif status == "Overdue":
                penalty = round(base_tax * 0.12, 2) # 12% statutory interest/penalty
                total_due = round(base_tax + penalty, 2)
                pay_date = None
            else: # Unpaid
                penalty = 0.0
                total_due = base_tax
                pay_date = None
                
            authority = f"Gram Panchayat {v_name} Revenue Section" if "Agricultural" in l_use or "Forest" in l_use else f"{d_name} Urban Development Authority / Municipal Council"
            
            tax_rows.append({
                "tax_id": tax_id,
                "parcel_id": p_id,
                "simulated_ulpin": ulpin,
                "financial_year": fy,
                "taxable_value_inr": taxable_val,
                "tax_amount_inr": base_tax,
                "penalty_inr": penalty,
                "total_payable_inr": total_due,
                "payment_status": status,
                "payment_date": pay_date if pay_date else "N/A",
                "tax_authority": authority,
                "data_status": config.DATA_STATUS["SYNTHETIC"],
                "provenance": "Synthetic municipal / panchayat property tax assessment"
            })
            
    df_tax = pd.DataFrame(tax_rows)
    csv_out = tax_dir / "property_tax.csv"
    df_tax.to_csv(csv_out, index=False)
    print(f"  -> Generated {len(df_tax)} property tax assessment records in {csv_out}")

if __name__ == "__main__":
    generate_property_tax()
