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
        df = df[['Location', 'Abbreviation', 'Statutory Limit on Abortions']]
        sort_order = ["Abortion banned", "Fetal viability", "6 weeks LMP", "12 weeks LMP", "18 weeks LMP", 
                      "22 weeks LMP", "24 weeks LMP", "3rd trimester"]
        
        df['sort_order'] = df['Statutory Limit on Abortions'].apply(lambda x: sort_order.index(x) if x in sort_order else len(sort_order))
        df = df.sort_values(by= 'sort_order')
    
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

    fig = px.choropleth(locations = 'Abbreviation', locationmode="USA-states", scope="usa",
                        color = 'Statutory Limit on Abortions', hover_data = 'Location',
                        color_discrete_sequence = ["#D95319", "#F2801E", "#FBAF5F", "#D8D8D8", "#A3D0F2", "#5AB4F2", "#1E69D2", "#00298C"],
                        title = "Statutory limit on abortions by state",
                        data_frame = df)
    
    return fig

def run_app():
    """ 
    Using dash, display maps
    """
    mortality_map = map_mortalities()
    mortality_data = load_data(DEATHS, False)

    abortion_map = map_abortion_laws()
    abortion_data = load_data(ABORTION_LAWS, True)

    app = Dash()
    app.layout = html.Div([
        html.H4("Analysis of maternal mortality rates and abortion legislation"),
        dcc.Graph(figure=mortality_map),
        dcc.Graph(figure=abortion_map),
        #dash_table.DataTable(data=mortality_data.to_dict('records'), page_size=10)
    ])

    app.run_server(debug=True, use_reloader=False)
    

if __name__ == '__main__':
    run_app()