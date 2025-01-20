# Women in Stem

## Members

- Elizabeth Ronan <eronan@uchicago.edu>
- Dorothy Wongkarnta <dwongkarnta@uchicago.edu>
- Madelin De Jesus Martinez <madelin@uchicago.edu>
- Alexandrea Harriott <aharriott@uchicago.edu>

## Abstract

Our research question is as follows: how does racism, education, poverty, and other demographics affect outcomes for pregnant women in the United States? We want to explore data at a state level to analyze maternal mortality across the US, exploring related characteristics such as the utilization of midwives and demographic characteristics of mothers from CDC data. We plan to create interactive visualizations, including tables and maps, exploring maternal death rates and these associated characteristics. We plan to run a regression on our data to see trends in maternal mortality, broken down by demographic characteristics, as well as potentially to predict how certain policy interventions may change these trends over time.

## Preliminary Data Sources

For each source please add a section with the following:

### Data Source #1: {Maternal Death Rate By State}

- [CDC Maternal Mortality Data -- Summary Level](https://www.cdc.gov/nchs/maternal-mortality/data.htm)
- This data is from a web page
- We hope to find data at the individual level (with demographic data and state data). If we cannot find this data, we will find state or county level data and then pull in census data with demographics to compare and contrast by demographic and location. See database [here](https://wonder.cdc.gov/).

### Data Source #2: {Census Data}
- [Census Web Page](https://data.census.gov/table)
- This data is from a web page
- The use of this data depends on the geographic granularity we are able to find in CDC data for deaths. We plan to use this data, matched on location, to map maternal death rates with demographic characteristics of that geographic level. We also plan to use census shapefiles to visualize this analysis in maps.

### Data Source #2: {Midwife Use by State}
- Appendix three of [this report](https://www.gao.gov/assets/gao-23-105861.pdf)
- This data is from a web page (pdf report)
- We hope to find a better data source for the percent of midwife attended births at our selected geographical level or to locate where this report is getting this data.

## Preliminary Project Plan
We will need to ingest data from multiple sources, clean the data for any NA columns or missing data, across all our data sources find a common geographic level, then merge all of the data together. From here, we'll create interactive maps and tables to demonstrate current and historical rates of maternal mortality, then have those tables reflect the outcomes predicted by our model when introducing policy changes.

Our current plan is for Elizabeth and Dorothy to look into more robust data sources. Alexandrea and Madelin will work on ingesting our current data sources for preliminary data exploration.

## Questions
1) When should we settle on final data sources? How late in the game can we change our sources?
2) What is the difference between web page data and bulk data?
3) Have previous projects used the CDC Wonder data portal?
