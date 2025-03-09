from pathlib import Path
from mortality.utils import STATE_ABBREVIATIONS
import pandas as pd

'''In this file, we are using the scraped data from the KFF website, and we are 
merging a few columns for our map. 

This merge uses the state column as the unique identifier, to ensure that we are
matching the data correctly, across csv files. 

During the merge, a few cleaning steps were taking, to ensure the data is legible
and consisten when presented in the map. 
'''

# paths to the files we are merging
maternal_mortality_path = Path(__file__).parent.parent.joinpath(
    "data/scrape_data/kff_maternal_mortality.csv"
)
coverage_path = Path(__file__).parent.parent.joinpath(
    "data/scrape_data/kff_coverage.csv"
)
earnings_path = Path(__file__).parent.parent.joinpath(
    "data/scrape_data/kff_earnings.csv"
)
cesarean_path = Path(__file__).parent.parent.joinpath(
    "data/scrape_data/kff_cesarean.csv"
)

# path we are creating for new csv
merged_kff = Path(__file__).parent.parent.joinpath("data/scrape_data/merged_kff.csv")

# loading the csv files
mortality = pd.read_csv(maternal_mortality_path)
coverage = pd.read_csv(coverage_path)
earnings = pd.read_csv(earnings_path)
cesarean = pd.read_csv(cesarean_path)

# cleaning files: earnings
earnings["women_weekly"] = (
    earnings["women_weekly"]
    .astype(str)
    .str.replace(r"[\$,]", "", regex=True)
    .astype(float)
)
earnings["ratio_earings_to_men"] = (
    earnings["ratio"].astype(str).str.rstrip("%").astype(float) / 100
)

# cleaning files: coverage
coverage.rename(
    columns={"Employer": "state"}, inplace=True
)  # rename column for merging
coverage["Uninsured"] = (
    coverage["Uninsured"].astype(str).str.rstrip("%").astype(float) / 100
)  # Convert Uninsured to decimal

# extracting specific columns
mortality = mortality[["state", "Maternal Mortality Rate per 100,000 live Births"]]
coverage = coverage[["state", "Uninsured"]]
earnings = earnings[["state", "women_weekly", "ratio_earings_to_men"]]
cesarean = cesarean[["state", "cesarean"]]

# merging all data on state column
merged_df = (
    mortality.merge(coverage, on="state", how="inner")
    .merge(earnings, on="state", how="inner")
    .merge(cesarean, on="state", how="inner")
)

# adding the column of abbreviation from dictionary "STATE_ABBREVIATION"
merged_df["state_abbreviation"] = merged_df["state"].map(STATE_ABBREVIATIONS)

# saving the merged data
merged_df.to_csv(merged_kff, index=False)
