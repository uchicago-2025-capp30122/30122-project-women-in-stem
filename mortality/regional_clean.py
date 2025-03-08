import csv
from pathlib import Path

#Cleaning Regional data
region_path_open = Path(__file__).parent.parent.joinpath("data/downloaded_data/region_age_educ_race.csv")
region_path_write = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
fieldnames = ['region', 'race', 'education', 'ten_year_age_groups', 'deaths', 'percent_total_deaths']


# Read the CSV file
with open(region_path_open, 'r', encoding='utf-8') as file:
    content = list(csv.DictReader(file))

# Write the cleaned data
with open(region_path_write, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in content:
        cleaned_row = {
            'region': row['Census Region'].strip().lower()[17:],
            'race': row['Single Race 6'].strip().lower(),
            'education': row['Education'].strip().lower().replace('?', "'") if row['Education'] != 'Not Available' else 'unknown',
            'ten_year_age_groups': row['Ten-Year Age Groups Code'].strip().lower(),
            'deaths': row['Deaths'].strip().lower(),
            'percent_total_deaths': float(row['% of Total Deaths'].strip().lower()[:3])
        }
        writer.writerow(cleaned_row)
        