# Women in Stem

## Abstract
Our research question is as follows: how does race/ethnicity, income, poverty, and other demographics affect outcomes for pregnant people in the United States? How do abortion laws affect outcomes for pregnant people, and how will policy changes impact these outcomes? We want to explore data at a state level to analyze maternal mortality across the US, exploring related characteristics from the KFF (and CDC Wonder) and NY Times. We plan to create an interactive map visualization that will show summary statistics for different states exploring maternal mortality with associated characteritics.

Additionally, we plan to create a background regression model where we see the effect of interested characteristics on maternal mortality rate. The user wil be able to put their own demographics into a python program, and it will show the predicted maternal mortality rate using the regression model output. This can be helpful for the user to consider their current situation in their state or another state with varying access levels to abortion.  

## Data Sources

### Data Reconciliation Plan
There are 3 data sources that we will working with for this project, where each data source will have the information about each state in the U.S. In other words, the "unqiue" key for each data is the "STATE". In this case, we can join every data source. The information about each data source is as followed:

### Data Source #1 : [Maternal Mortality Data](https://www.commonwealthfund.org/publications/scorecard/2024/jul/2024-state-scorecard-womens-health-and-reproductive-care) 
- This data source has the [CDC wonder data](https://wonder.cdc.gov/) as a foundation.
- This data is from a webpage, but there is bulk data available and ready for download.
- From this data source, we aim to use the summary statistics provided by the second green map. This data lives in a CSV file, composed of 51 rows, representing all 50 states and the District of Columbia, and 5 columns. 
- We plan to use the column labelled as "0–18.6" which refers to the maternal mortality rates per 100,000 live births.

### Data Source #2: [Women's Demographics](https://www.kff.org/interactive/womens-health-profiles/alaska/demographics/)
- This data source has the [CDC wonder data](https://wonder.cdc.gov/) as a foundation.
- This second data source will fulfill the web scraping portion of the project. We will be pulling data from the "demographics", "coverage", and "maternal and infant health" sections. 
- This is coming from a webpage where we have to scape some charactersitics, but some might have bulk data ready to download (e.g. web scraping for incomes within "demographics", but data download for "coverage").
- The main challenge for this data is that many of the data has to be scraped through the interactive component which we don't have exposure to (also a part of our question at the end).
- There should be total of 50 records after the web-scraping.
- There should be at least 4 columns corresponding to each characteristic (race, incomes, poverty, health insurance, etc). We might add additional charatersitics as we see fit through the selection process.
- The webpage only shows the information about each state one at a time, where each state contains different factors that we are interested in. Therefore, our main issue is about navigating each state to get the data.  

### Data Source #3: [Abortion Ban Across the Country](https://www.nytimes.com/interactive/2024/us/abortion-laws-roe-v-wade.html) 
- This data is coming from a webpage where we have to scrape the status of each state. 
- We has this data as a backup for additional charactersitics that we might use for creating summary statistics and the regression model.
- There should 50 records (the same as the number of the U.S. state).
- There will be only one column (the abortion status) where we might want to combine with Data source 1 and 2.
- We inspected the html structure of the page and we plan to scrape the state and its abortion status from the state detail table where we plan to keep the category levels as is.

## Project Plan
Meet weekly to discuss findings and new tasks: 
- Week 1: Start/finish with the KFF data scraping and ingesting bulk data (Alex)
- Week 2: Clean and combine data (Madelin)
- Week 3: Milestone 3 due; start python programming and mapping (Liz)
- Week 4-5: Finish program (Dorothy)
- Week 6: Final edits (Alex)

## Questions
1. Is it okay if we use data that is already cleaned for us (For example, the KFF gets the data from the CDC Wonder, but they stratified the data already in the way we can just pull to use)? (We might end up using CDC Wonder, but for now KFF Data is our best option).
2. For interactive data, how does it change our web scraping strategy? (For example, in our first data source, we have to click/hover on each state to access the information on that state. We looked at the page source and it has a data-type=”interactive”, and there’s a link to a https with .js, which we assume is javascript.)