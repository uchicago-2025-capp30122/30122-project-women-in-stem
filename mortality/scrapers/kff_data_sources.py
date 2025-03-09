"""
The dictionary that contains all of the necessary information needed to scrape
all of the data sources. This allows for easy addition of data. Note that
all of these data sources come from the Kaiser Family Foundation and follow
the same format, where the data of interest is first within a dictionary with
'data' being the key, and then contained in a list of lists, with each list
being a state. Each url was found by inspecting site and finding the urls
containing relevant data within the network tab.

Women's Demographics (dem):
    https://www.kff.org/interactive/womens-health-profiles/alabama/demographics/

Maternal and Infant Health (mih):
    https://www.kff.org/interactive/womens-health-profiles/alaska/maternal-infant-health/

Coverage (cov):
    https://www.kff.org/interactive/womens-health-profiles/alaska/healthcare-coverage/

Each key (str), value (tuple) pair of the dictionary follows the format below.
    (three-letter code for which category source falls under) Name of data:
    (url to data,
    variable names for each row of data,
    the index in the list of lists you would like to start pulling data from,
    the path and name to the output file)
"""

DATA_SOURCES = {
    "(dem) Distribution of Women Ages 18-64, by Race/Ethnicity": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Race%20Distribution",
        [
            "state",
            "total",
            "white",
            "black",
            "hispanic",
            "asian",
            "nhopi",
            "aian",
            "other",
        ],
        2,
        "data/scrape_data/kff_race.csv",
    ),
    "(dem) Distribution of Women Ages 19 to 64, by Age Group, 2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Age%20distribution",
        ["state", "total", "age19_25", "age26_34", "age35_54", "age55_64"],
        2,
        "data/scrape_data/kff_age.csv",
    ),
    "(dem) Distribution of Women Ages 18-64, by Federal Poverty Level, 2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=FPL%20distribution",
        ["state", "total", "fplless_100", "fpl100_199", "fpl200_399", "fplmore_400"],
        2,
        "data/scrape_data/kff_poverty.csv",
    ),
    "(dem) Median Weekly Earnings for Women and Men, 2021": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Median%20Weekly%20Earnings",
        ["state", "women_weekly", "men_weekly", "ratio"],
        2,
        "data/scrape_data/kff_earnings.csv",
    ),
    "(mih) Infant Mortality Rate, 2020-2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Infant%20Mortality",
        ["state", "2020", "2021", "2022", "2023"],
        2,
        "data/scrape_data/kff_infant_mortality.csv",
    ),
    "(mih) Infant Mortality Rate by Race/Ethnicity, 2020-2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Infant%20Mortality%20R/E",
        ["state", "white", "black or african american", "hispanic", "other"],
        1,
        "data/scrape_data/kff_infant_mortality_re.csv",
    ),
    "(mih) Maternal Deaths and Mortality Rates per 100,000 live births, 2018-2021": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Maternal%20Mortality",
        [
            "state",
            "number of deaths",
            "Maternal Mortality Rate per 100,000 live Births",
        ],
        1,
        "data/scrape_data/kff_maternal_mortality.csv",
    ),
    "(mih) Cesarean Deliveries as a Percentage of All Births, 2021": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=C-section%20Births",
        ["state", "cesarean", "low-risk cesarean"],
        2,
        "data/scrape_data/kff_cesarean.csv",
    ),
    "(mih) Cesarean Deliveries as a Percentage of All Births by Race/Ethnicity, 2021": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=C-sections%20RaceEthnicity",
        ["state", "white", "black", "hispanic"],
        2,
        "data/scrape_data/kff_cesarean_re.csv",
    ),
    "(cov) Health Insurance Coverage of Women Ages 19-64, 2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Insurance%20Coverage%2019-64",
        ["Employer", "Non-Group", "Medicaid", "Other", "Uninsured"],
        2,
        "data/scrape_data/kff_coverage.csv",
    ),
    "(cov) Uninsured Rates of Women Ages 19-64, 2010–2023": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Uninsured%20Rates%2019-64",
        [
            "state",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
        ],
        2,
        "data/scrape_data/kff_uninsured.csv",
    ),
    "(cov) Status of State Action on the Medicaid Expansion Decision, as of November 2024": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=ACA%20Medicaid%20Expansion",
        ["state", "Status of Medicaid Expansion Decision"],
        2,
        "data/scrape_data/kff_medicaid_expansion.csv",
    ),
    "(cov) Status of Medicaid Postpartum Coverage Extensions, as of January 6, 2025": (
        "https://www.kff.org/wp-json/kff/v1/google-sheets-tab?id=1PVDm79MNXt2mj_gZijrEgoQEEj1Koh0Ur9ZV-MrmgYQ&tab=Postpartum%20Extension",
        ["state", "status of state action"],
        1,
        "data/scrape_data/kff_postpartum_coverage.csv",
    ),
}
