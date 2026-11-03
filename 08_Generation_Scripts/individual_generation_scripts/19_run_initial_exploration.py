"""
19_run_initial_exploration.py
Wrapper executing the Initial Data Exploration pipeline.
"""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT / "06_Initial_Data_Exploration"))

from initial_data_exploration import run_exploration

if __name__ == "__main__":
    run_exploration()
