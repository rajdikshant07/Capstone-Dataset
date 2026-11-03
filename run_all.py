"""
run_all.py
Land Stack: Integrated GIS-Based Digital Public Infrastructure for Land Governance
Module 1: Data Acquisition and Dataset Preparation
Master Orchestration Pipeline

Executes all 20 generation, exploration, and validation modules in sequence,
verifying dependencies, timing execution, and logging all metrics.
"""

import sys
import os
import time
import datetime
from pathlib import Path

# Ensure paths
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "08_Generation_Scripts" / "individual_generation_scripts"))
sys.path.append(str(PROJECT_ROOT / "06_Initial_Data_Exploration"))
sys.path.append(str(PROJECT_ROOT / "07_Data_Quality"))
sys.path.append(str(PROJECT_ROOT / "03_ULPIN_Simulation"))

import config

def log_msg(msg: str, log_file=None):
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

def main():
    start_time = time.time()
    log_dir = config.SCRIPTS_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "generation_pipeline.log"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== LAND STACK MODULE 1 PIPELINE EXECUTION LOG ===\nStarted: {datetime.datetime.now().isoformat()}\n\n")
        
    log_msg("================================================================================", log_file)
    log_msg("  LAND STACK: DIGITAL PUBLIC INFRASTRUCTURE FOR LAND GOVERNANCE", log_file)
    log_msg("  MODULE 1 - COMPLETE SYNTHETIC DATA GENERATION & VALIDATION PIPELINE", log_file)
    log_msg("================================================================================", log_file)
    log_msg(f"Target Configuration: 3 States, 15 Districts, 75 Villages", log_file)
    log_msg(f"Total Target Parcels: {config.TOTAL_PARCELS:,} | Random Seed: {config.RANDOM_SEED}", log_file)
    log_msg(f"Coordinate Reference System: {config.CRS_NAME}", log_file)
    log_msg("--------------------------------------------------------------------------------", log_file)
    
    pipeline_steps = [
        ("Administrative Geography", "01_generate_administrative.py", "01_generate_administrative", "generate_administrative_layers"),
        ("Cadastral Land Parcels", "02_generate_parcels.py", "02_generate_parcels", "generate_parcels"),
        ("Survey Numbers & Formats", "03_generate_survey_numbers.py", "03_generate_survey_numbers", "generate_survey_records"),
        ("Simulated ULPIN Records", "04_generate_ulpin.py", "04_generate_ulpin", "generate_ulpin_dataset"),
        ("Land Use & Land Cover", "05_generate_land_use.py", "05_generate_land_use", "generate_land_use"),
        ("Road Network Infrastructure", "06_generate_roads.py", "06_generate_roads", "generate_roads"),
        ("Hydrological Water Bodies", "07_generate_water_bodies.py", "07_generate_water_bodies", "generate_water_bodies"),
        ("Utility Infrastructure", "08_generate_utilities.py", "08_generate_utilities", "generate_utilities"),
        ("Ownership Records", "09_generate_ownership.py", "09_generate_ownership", "generate_ownership"),
        ("Record of Rights (RoR)", "10_generate_ror.py", "10_generate_ror", "generate_ror"),
        ("Property Registration", "11_generate_registration.py", "11_generate_registration", "generate_registration"),
        ("Property Tax Assessments", "12_generate_property_tax.py", "12_generate_property_tax", "generate_property_tax"),
        ("Mortgages & Encumbrances", "13_generate_mortgages.py", "13_generate_mortgages", "generate_mortgages"),
        ("Building Permits", "14_generate_building_permits.py", "14_generate_building_permits", "generate_building_permits"),
        ("Land Restrictions", "15_generate_land_restrictions.py", "15_generate_land_restrictions", "generate_land_restrictions"),
        ("Audit History Trail", "16_generate_audit_history.py", "16_generate_audit_history", "generate_audit_history"),
        ("State Mapping Templates", "17_generate_state_mapping.py", "17_generate_state_mapping", "generate_state_mapping_artifacts"),
        ("Dataset Source Log", "18_generate_source_log.py", "18_generate_source_log", "generate_source_documentation"),
        ("Dataset Inventory (21 Sheets)", "19_generate_dataset_inventory.py", "19_generate_dataset_inventory", "generate_inventory"),
        ("Initial Data Exploration", "initial_data_exploration.py", "initial_data_exploration", "run_exploration"),
        ("Automated Quality Checks", "data_quality_checks.py", "data_quality_checks", "run_quality_checks")
    ]
    
    for idx, (label, script_name, mod_name, fn_name) in enumerate(pipeline_steps, start=1):
        step_start = time.time()
        log_msg(f"[{idx:02d}/{len(pipeline_steps):02d}] Executing: {label} ({script_name})...", log_file)
        try:
            mod = __import__(mod_name)
            func = getattr(mod, fn_name)
            func()
            elapsed = time.time() - step_start
            log_msg(f"      -> Completed {label} in {elapsed:.2f} seconds.", log_file)
        except Exception as e:
            log_msg(f"ERROR: Step {label} failed: {e}", log_file)
            import traceback
            log_msg(traceback.format_exc(), log_file)
            sys.exit(1)
            
    total_elapsed = time.time() - start_time
    log_msg("================================================================================", log_file)
    log_msg(f"SUCCESS: Complete Land Stack Module 1 Pipeline Finished in {total_elapsed:.2f}s", log_file)
    log_msg(f"Pipeline execution logs saved to: {log_file}", log_file)
    log_msg("================================================================================", log_file)

if __name__ == "__main__":
    main()
