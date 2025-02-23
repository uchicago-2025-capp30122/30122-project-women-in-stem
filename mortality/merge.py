
import csv
from pathlib import Path

'''
Code to merge mortality rate and health systems csv 
'''
MERGED_COLUMNS = ["state", "mortality_rate", "unknown_mortality", "performance_category", "unknown_performance"]

mrt_path = Path("data/mortality_rate.csv")
hlthsys_path = Path("data/health system performance for women.csv")
merged_path = Path("data/merged_data.csv")

# read mortality into a dictionary
mortality_data = {}
with open(mrt_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        state = row["state"]
        mortality_data[state] = {
            "mortality_rate": row["mortality_rate"],
            "unknown_mortality": row["unknown"]
        }

# merger with health systems
merged_data = []
with open(hlthsys_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        state = row["state"]
        
        mortality_info = mortality_data.get(state, {})
        
        merged_data.append({
            "state": state,
            "mortality_rate": mortality_info.get("mortality_rate"),
            "unknown_mortality": mortality_info.get("unknown_mortality"),
            "performance_category": row["performance_category"],
            "unknown_performance": row["unknown"]
        })


with open(merged_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=MERGED_COLUMNS)
    writer.writeheader()
    writer.writerows(merged_data)









