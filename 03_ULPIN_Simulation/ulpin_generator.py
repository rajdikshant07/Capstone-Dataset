"""
ulpin_generator.py
Land Stack: Simulated ULPIN (Unique Land Parcel Identification Number) Generator
Module: 03_ULPIN_Simulation

IMPORTANT DISCLAIMER:
The identifiers produced by this module are SIMULATED demonstration identifiers for the
Land Stack academic project. They do NOT claim to represent or comply with the official
Government of India Bhu-Aadhaar / ULPIN production specification or official cadastre.
"""

import hashlib
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Set

# Base36 alphabet (0-9, A-Z)
BASE36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class SimulatedULPINGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.generated_ulpins: Set[str] = set()
        self.collision_count = 0
        
    def _int_to_base36(self, num: int, length: int = 7) -> str:
        """Converts an integer to a fixed-length Base36 alphanumeric string."""
        res = []
        while num > 0:
            num, rem = divmod(num, 36)
            res.append(BASE36[rem])
        s = "".join(reversed(res)) if res else "0"
        return s.rjust(length, "0")[-length:]
        
    def generate_ulpin(
        self,
        state_code: str,
        district_code: str,
        village_code: str,
        centroid_lat: float,
        centroid_lon: float,
        parcel_seq: int
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generates a 14-character simulated ULPIN:
        - Chars 1-2: State LGD Code (2 numeric digits)
        - Chars 3-4: District Code (2 numeric digits)
        - Chars 5-7: Village Code (3 numeric digits)
        - Chars 8-14: 7-character Base36 spatial hash of coordinates + parcel seq + seed
        """
        st_code = str(state_code).zfill(2)[:2]
        dist_code = str(district_code).zfill(2)[:2]
        vil_code = str(village_code).zfill(3)[:3]
        prefix = f"{st_code}{dist_code}{vil_code}"  # 7 chars
        
        attempt = 0
        while True:
            hash_input = f"{self.seed}:{st_code}:{dist_code}:{vil_code}:{centroid_lat:.6f}:{centroid_lon:.6f}:{parcel_seq}:{attempt}"
            hash_digest = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
            # Convert first 10 hex chars to integer, then to 7 base36 chars
            hash_int = int(hash_digest[:10], 16)
            suffix = self._int_to_base36(hash_int, length=7)
            
            candidate_ulpin = f"{prefix}{suffix}"
            assert len(candidate_ulpin) == 14, f"ULPIN length must be 14, got {len(candidate_ulpin)}"
            
            if candidate_ulpin not in self.generated_ulpins:
                self.generated_ulpins.add(candidate_ulpin)
                break
            else:
                self.collision_count += 1
                attempt += 1
                
        meta = {
            "ulpin": candidate_ulpin,
            "state_code": st_code,
            "district_code": dist_code,
            "village_code": vil_code,
            "generation_method": "DETERMINISTIC_GEO_BASE36_SIMULATION",
            "generation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "uniqueness_status": "GUARANTEED_UNIQUE_IN_DATASET",
            "data_status": "SIMULATED",
            "official_claim_disclaimer": "Simulated identifier for demonstration; not official GoI ULPIN."
        }
        return candidate_ulpin, meta

def validate_ulpins(ulpin_list: list) -> Dict[str, Any]:
    """Validates uniqueness, length and alphanumeric integrity of generated ULPINs."""
    total = len(ulpin_list)
    unique_count = len(set(ulpin_list))
    format_valid = all(len(u) == 14 and u.isalnum() and u.isupper() for u in ulpin_list)
    
    report = {
        "total_records": total,
        "unique_records": unique_count,
        "duplicate_count": total - unique_count,
        "is_100_percent_unique": total == unique_count,
        "all_14_chars_alphanumeric": format_valid,
        "validation_status": "PASSED" if (total == unique_count and format_valid) else "FAILED",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    return report

if __name__ == "__main__":
    gen = SimulatedULPINGenerator(seed=42)
    sample_ulpin, meta = gen.generate_ulpin("27", "01", "001", 18.5204, 73.8567, 1)
    print("Sample Simulated ULPIN:", sample_ulpin)
    print("Metadata:", json.dumps(meta, indent=2))
