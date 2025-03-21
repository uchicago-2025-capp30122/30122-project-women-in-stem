import csv
from pathlib import Path

HLTHSYS_CSV_COLUMNS = ("state", "performance_category", "unknown")
MORTRATE_CSV_COLUMNS = ("state", "mortality_rate", "unknown")

"""
Cleaning the mortality rate csv
"""
mrt_path = Path("data/mortality_rate.csv")
cleaned_data = []

with open(mrt_path, 'r', newline='') as csvfile: 
    reader = csv.reader(csvfile)

    for row in reader:
        state = row[0].lower().strip()
        mortality_rate = row[2].strip()

        if "data not available" in mortality_rate.lower():
            mortality_rate = None
        else:
            mortality_rate = mortality_rate.replace('–', '-')  # replaces en-dash with hyphen
        
        cleaned_data.append({
            "state": state,
            "mortality_rate": mortality_rate,
            "unknown": row[3]  # keeping the unknown column as is until we figure out what it stands for 
        })

with open(mrt_path, 'w', newline='') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames=MORTRATE_CSV_COLUMNS)
    writer.writeheader()
    writer.writerows(cleaned_data)


"""
Cleaning the health systems performance csv
"""
hlthsys_path = Path("data/health system performance for women.csv")
cleaned_row = []

with open(hlthsys_path, 'r') as csvfile: 
    reader = csv.reader(csvfile)
    
    for row in reader:
        state = row[0].lower().strip()
        category = row[2].lower().strip().replace('–', '-')  # replaces en-dash with hyphen
        unknown = row[3].strip()

        cleaned_row.append({
            "state": state,
            "performance_category": category,
            "unknown": unknown
        })

# Write the cleaned data
with open(hlthsys_path, 'w', newline='') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames=HLTHSYS_CSV_COLUMNS)
    writer.writeheader()
    writer.writerows(cleaned_row)