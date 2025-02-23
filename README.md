# U.S. Maternal Mortality

### Author: 
[Elizabeth Ronan](https://github.com/elizabethronan)
[Dorothy Wongkarnta](https://github.com/Donlapun)
[Madelin De Jesus Martinez](https://github.com/madelindejesus)
[Alexandrea Harriott](https://github.com/a-harriott)

# Summary

Our research question is as follows: 
- How does race/ethnicity, income, poverty, and other demographics affect outcomes for pregnant people in the United States? 
- How do abortion laws affect outcomes for pregnant people, and how will policy changes impact these outcomes? 

We want to explore data at a state level to analyze maternal mortality across the US, exploring related characteristics from the KFF (and CDC Wonder) and NY Times. We plan to create an interactive map visualization that will show summary statistics for different states exploring maternal mortality with associated characteritics.

Additionally, we plan to create a background regression model where we see the effect of interested characteristics on maternal mortality rate. The user wil be able to put their own demographics into a python program, and it will show the predicted maternal mortality rate using the regression model output. This can be helpful for the user to consider their current situation in their state or another state with varying access levels to abortion.

# How to run the Appplication

1. Clone the repository using this command: 

`git clone git@github.com:uchicago-2025-capp30122/30122-project-women-in-stem.git`

2. Run the scrapers to get the data : 

`uv run python -m mortality.scrapers`

3. To execute the program choose either of the followings:

`uv run python -m mortality map` - to run the visualization map
`uv run python -m mortality prediction` - to run the visualization map

Please follow the prompts right once the program starts

# Data Source
[2024 State Scorecard on Women’s Health and Reproductive Care](https://www.commonwealthfund.org/publications/scorecard/2024/jul/2024-state-scorecard-womens-health-and-reproductive-care)

[KFF State Profiles for Women’s Health](https://www.kff.org/interactive/womens-health-profiles/alaska/demographics/)






