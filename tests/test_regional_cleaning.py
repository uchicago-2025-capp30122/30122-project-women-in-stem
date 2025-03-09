import csv
from pathlib import Path
import pandas as pd
import pytest
import mortality.regional_clean

@pytest.fixture
def regional_clean_df():
    file = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
    mortality_data = pd.read_csv(file)
    return mortality_data

# check mortality rate is floar and between 1 AND 0
# ince clean, make sure there is no ? or . 
# rows ==  120 after cleaned, so I shouldnt lose or gain any new rows. 