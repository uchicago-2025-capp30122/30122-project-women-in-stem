import pandas as pd
from pathlib import Path
import plotly.express as px
from dash import Dash, dcc, html, dash_table

# # From this data source, we aim to use the summary statistics provided by the 
# # second green map. This data lives in a CSV file, composed of 51 rows, 
# # representing all 50 states and the District of Columbia, and 5 columns. 
# # We plan to use the column labelled as "0–18.6" which refers to the maternal 
# # mortality rates per 100,000 live births.

DEATHS = Path(__file__).parent.parent.joinpath("data/scrape_data/deaths.csv")
ABORTION_LAWS = Path(__file__).parent.parent.joinpath("data/scrape_data/abortion.csv")

def load_data(file, abortion):
    """
    Loads in the example CSV for visualizations

    Inputs: none
    Outputs: Pandas dataframe
    """

    df = pd.read_csv(file)
    
    if abortion:
        df = df[['Location', 'Statutory Limit on Abortions']]
    
    else:
        df = df[['state', 'abbrev', 'deaths', 'lower', 'upper']]
        df = df.sort_values(by=['lower'], ascending=False)
        df.columns = ['State', 'Abbreviation', 'Deaths', 'Lower Estimate', 'Upper Estimate']

    return df

def map_mortalities():
    """
    Creates a chloropleth map by state of maternal mortalities
    """
    df = load_data(DEATHS, False)

    fig = px.choropleth(locations= 'Abbreviation', locationmode="USA-states", scope="usa",
                        color = 'Deaths', hover_data= 'State',
                        color_discrete_sequence = ["#084594", "#4292c6", "#9ecae1", "#c6dbef"],
                        title = 'Deaths per 100,000 female population by state',
                        data_frame=df)
    
    return fig

def map_abortion_laws():
    df = load_data(ABORTION_LAWS, True)

    #fig = px.choropleth(locations = )

def run_app():
    """ 
    Using dash, display maps
    """
    mortality_map = map_mortalities()
    mortality_data = load_data(DEATHS, False)

    abortion_data = load_data(ABORTION_LAWS, True)
    print(abortion_data)

    #mortality_map.show()

    # app = Dash()
    # app.layout = html.Div([
    #     dcc.Graph(figure=mortality_map),
    #     dash_table.DataTable(data=mortality_data.to_dict('records'), page_size=10)
    # ])

    # app.run_server(debug=True, use_reloader=False)
    

if __name__ == '__main__':
    run_app()