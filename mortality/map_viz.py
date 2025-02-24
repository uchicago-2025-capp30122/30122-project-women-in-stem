import pandas as pd
from pathlib import Path
import plotly.express as px

def load_data():
    """
    Loads in the example CSV for visualizations

    Inputs: none
    Outputs: Pandas dataframe
    """
    file = Path(__file__).parent.parent.joinpath("data/scrape_data/deaths.csv")

    df = pd.read_csv(file)
    df = df[df['state'] != 'district of columbia']

    return df

def map_mortalities():
    df = load_data()
    fig = px.choropleth(locations= 'abbrev', locationmode="USA-states", scope="usa",
                        color = 'lower', hover_data= 'state', 
                        color_continuous_scale=px.colors.sequential.Blues,
                        title='Deaths per 100,000 female population by state',
                        data_frame=df)
    fig.show()
    
map_mortalities()


# def load_shapefile():
#     """
#     Loads in a shapefile of US states
#     """
#     file = "data/shapefiles/tl_2024_us_state/ts_2024_us_state.shp"
#     shp_path = Path(__file__).parent.parent.joinpath(file)

#     states = {}

#     with shapefile.Reader(shp_path) as sf:
#         for shape_rec in sf.shapeRecords():
#             # shape_rec.shape.points - list of WKT points, used to construct
#             #                             a shapely.Polygon
#             # We are assuming Polygon here! If this file had points/lines/etc.
#             # changes would be needed.
#             polygon = Polygon(shape_rec.shape.points)
#             # shape_rec.record contains the attributes as a list or dictionary
#             # in this file record[0] contains the neighborhood name
#             name = shape_rec.record[0]
#             # associate polygon with name
#             states[name] = polygon
            
#     return states

# # From this data source, we aim to use the summary statistics provided by the 
# # second green map. This data lives in a CSV file, composed of 51 rows, 
# # representing all 50 states and the District of Columbia, and 5 columns. 
# # We plan to use the column labelled as "0–18.6" which refers to the maternal 
# # mortality rates per 100,000 live births.