import csv
from pathlib import Path

#Cleaning Regional data
region_path_open = Path(__file__).parent.parent.joinpath("data/downloaded_data/region_age_educ_race.csv")
region_path_write = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
fieldnames = ['region', 'race', 'education', 'ten_year_age_groups', 'deaths', 'mortality_rate', 'mortality_binary']


# Read the CSV file
with open(region_path_open, 'r', encoding='utf-8') as file:
    content = list(csv.DictReader(file))

# Write the cleaned data
with open(region_path_write, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in content:
        mortality_rate = (float(row['% of Total Deaths'].strip().lower()[:3]))
        
        #creates mortality rate into a binary variable
        if mortality_rate > 0.001: 
            mortality_binary = 1
        else: 
            mortality_binary = int(0)

        cleaned_row = {
            'region': row['Census Region'].strip().upper()[17]+ row['Census Region'].strip().lower()[18:],
            'race': row['Single Race 6'].strip(),
            'education': row['Education'].strip().replace('?', "'").replace(".", "") if row['Education'] != 'Not Available' else 'unknown',
            'ten_year_age_groups': row['Ten-Year Age Groups Code'].strip().lower(),
            'deaths': row['Deaths'].strip().lower(),
            'mortality_rate': round(mortality_rate/100, 3),
            'mortality_binary' : mortality_binary
        }
        writer.writerow(cleaned_row)

