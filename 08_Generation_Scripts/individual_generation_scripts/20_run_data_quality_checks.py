"""
20_run_data_quality_checks.py
Wrapper executing the Data Quality Checks engine.
"""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT / "07_Data_Quality"))

from data_quality_checks import run_quality_checks

if __name__ == "__main__":
    run_quality_checks()
