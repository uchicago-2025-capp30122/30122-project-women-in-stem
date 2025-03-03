import pandas as pd
from pathlib import Path
import plotly.express as px
from dash import Dash, dcc, html, dash_table

# # From this data source, we aim to use the summary statistics provided by the 
# # second green map. This data lives in a CSV file, composed of 51 rows, 
# # representing all 50 states and the District of Columbia, and 5 columns. 
# # We plan to use the column labelled as "0–18.6" which refers to the maternal 
# # mortality rates per 100,000 live births.

def load_data():
    """
    Loads in the example CSV for visualizations

    Inputs: none
    Outputs: Pandas dataframe
    """
    file = Path(__file__).parent.parent.joinpath("data/scrape_data/deaths.csv")

    df = pd.read_csv(file)
    df = df[df['state'] != 'district of columbia']
    df = df[['state', 'abbrev', 'deaths', 'lower', 'upper']]
    df = df.sort_values(by=['lower'], ascending=False)
    df.columns = ['State', 'Abbreviation', 'Deaths', 'Lower Estimate', 'Upper Estimate']

    return df

def map_mortalities():
    """
    Creates a chloropleth map by state of maternal mortalities
    """
    df = load_data()

    fig = px.choropleth(locations= 'Abbreviation', locationmode="USA-states", scope="usa",
                        color = 'Deaths', hover_data= 'State',
                        color_discrete_sequence = ["#084594", "#4292c6", "#9ecae1", "#c6dbef"],
                        title = 'Deaths per 100,000 female population by state',
                        data_frame=df)
    app = Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10)
    ])

    app.run_server(debug=True, use_reloader=False)
    
## Want to add option to display different demographics -- switch to merged data

if __name__ == '__main__':
    map_mortalities()