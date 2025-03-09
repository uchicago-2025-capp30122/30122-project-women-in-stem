import csv
from pathlib import Path
from mortality.utils import STATE_ABBREVIATIONS

# add state abbrevations as a column from utils import

#columns: 
# m 

# Columns:

# State
# kff_maternal_mortality "Maternal Mortality Rate per 100,000 live Births"
# kff_coverage Uninsured (remove % and divide by 100)
# kff_earnings women weekly (remove $)
# kff_cesarean cesarean

# Gotta make sure everything is for the same year



region_path_open = Path(__file__).parent.parent.joinpath("data/downloaded_data/region_age_educ_race.csv")
