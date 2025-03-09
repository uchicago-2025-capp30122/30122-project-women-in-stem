import pandas as pd
from pathlib import Path
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input

MERGED = Path(__file__).parent.parent.joinpath("data/merged_kff.csv")
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
        df = df.sort_values(by= 'sort_order').drop('sort_order', axis=1)
    
    else:
        df = df.sort_values(by=['mortality'], ascending=False)
        df.columns = ['State', 'Maternal Mortality Rate per 100,000 Live Births',
                       'Percent Uninsured', "Women's Average Weekly Earnings", 
                       "Ratio of Women's Earnings to Men's Earnings", "Percent Cesarean Births",
                       'Abbreviation']

    return df

def map_mortalities():
    """
    Creates a chloropleth map by state of maternal mortalities
    """
    df = load_data(MERGED, False).dropna()

    fig = px.choropleth(locations= 'Abbreviation', locationmode="USA-states", scope="usa",
                        color = 'Maternal Mortality Rate per 100,000 Live Births', 
                        custom_data= ['State', 'Maternal Mortality Rate per 100,000 Live Births'],
                        color_continuous_scale= px.colors.sequential.YlOrBr,
                        title = 'Maternal Mortality Rate per 100,000 Live Births by State',
                        data_frame=df)

    fig.update_traces(hovertemplate="<b>State:</b> %{customdata[0]}<br><b>Maternal Mortality Rate per 100,000 Live Births:</b> %{customdata[1]}<extra></extra>")
    
    return fig

def map_abortion_laws():
    """
    Creates a chloropleth map by state of statutory limits on abortion

    """
    df = load_data(ABORTION_LAWS, True)

    fig = px.choropleth(locations = 'Abbreviation', locationmode="USA-states", scope="usa",
                        color = 'Statutory Limit on Abortions',
                        custom_data=['Location', 'Statutory Limit on Abortions'],
                        color_discrete_sequence = ['#D95319', '#F2801E', '#A3D0F2', '#5AB4F2', '#3A9BE0', '#1E69D2', '#0045A2', '#001A70'],
                        title = "Statutory limit on abortions by state",
                        data_frame = df)
    
    fig.update_traces(hovertemplate="<b>State:</b> %{customdata[0]}<br><b>Limit:</b> %{customdata[1]}<extra></extra>")
    
    return fig

def run_app():
    """ 
    Using dash, display maps, table
    """

    app = Dash()
    app.layout = html.Div([
        html.H1("Analysis of Maternal Mortality Rates and Abortion Legislation", 
                style={'textAlign': 'left', 'fontSize': '32px', 'textDecoration': 'underline'}),
        html.Hr(),
        html.I("Please select the map and data you would like to view", style={'fontWeight': 'bold', 'marginBottom': '20px'}),
        dcc.RadioItems(options=["Maternal Mortality Rates", "Statutory Limits on Abortion"], 
                       value= 'Maternal Mortality Rates', id="map_select"),
        html.H4("Note: missing mortality data from 13 states."),
        dcc.Graph(figure= {}, id='map'),
        dash_table.DataTable(data= [], page_size=10, id='table')
    ])

    @callback(
        Output(component_id='map', component_property='figure'),
        Input(component_id='map_select', component_property='value')
    )
    def update_map(map):
        if map == 'Maternal Mortality Rates':
            return map_mortalities()
        return map_abortion_laws()
    
    @callback(
        Output(component_id='table', component_property='data'),
        Input(component_id='map_select', component_property='value')
    )
    def update_table(data):
        if data == 'Maternal Mortality Rates':
            return load_data(MERGED, False).to_dict('records')
        return load_data(ABORTION_LAWS, True).to_dict('records')


    app.run_server(debug=True, use_reloader=False)
    

if __name__ == '__main__':
    run_app()