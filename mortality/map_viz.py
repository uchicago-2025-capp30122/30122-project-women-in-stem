import pandas as pd
from pathlib import Path
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import statsmodels.api as sm

MERGED = Path(__file__).parent.parent.joinpath("data/merged_kff.csv")
ABORTION_LAWS = Path(__file__).parent.parent.joinpath("data/scrape_data/abortion.csv")


def load_data(file, abortion):
    """
    Loads in the example CSV for visualizations

    Inputs: none
    Outputs: Pandas dataframe
    """

    df = pd.read_csv(file)

    if abortion:  # if we're passing the abortion csv
        df = df[["Location", "Abbreviation", "Statutory Limit on Abortions"]]
        sort_order = [  # order from least restrictive to most restrictive
            "Fetal viability",
            "3rd trimester",
            "24 weeks LMP",
            "22 weeks LMP",
            "18 weeks LMP",
            "12 weeks LMP",
            "6 weeks LMP",
            "Abortion banned",
        ]

        df["sort_order"] = df["Statutory Limit on Abortions"].apply(
            lambda x: sort_order.index(x) if x in sort_order else len(sort_order)
        )
        df = df.sort_values(by="sort_order").drop("sort_order", axis=1)

    else:  # if we're passing the maternal mortality csv (merged)
        df = df.sort_values(by=["mortality"], ascending=False)
        df.columns = [
            "State",
            "Maternal Mortality Rate per 100,000 Live Births",
            "Percent Uninsured",
            "Women's Average Weekly Earnings",
            "Ratio of Women's Earnings to Men's Earnings",
            "Percent Cesarean Births",
            "Abbreviation",
        ]

        df[['Percent Uninsured']] = df[['Percent Uninsured']].astype(float)

    return df


def map_mortalities():
    """
    Creates a chloropleth map by state of maternal mortalities

    Inputs: none
    Outputs: plotly figure
    """
    df = load_data(MERGED, False).dropna()

    fig = px.choropleth(
        locations="Abbreviation",
        locationmode="USA-states",
        scope="usa",
        color="Maternal Mortality Rate per 100,000 Live Births",
        custom_data=["State", "Maternal Mortality Rate per 100,000 Live Births"],
        color_continuous_scale=px.colors.sequential.PuRd,
        title="Maternal Mortality Rate per 100,000 Live Births by State (2018-2021)",
        data_frame=df,
    )

    fig.update_traces(  # custom tooltip
        hovertemplate="<b>State:</b> %{customdata[0]}<br><b>Maternal Mortality Rate per 100,000 Live Births:</b> %{customdata[1]}<extra></extra>"
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Deaths per 100k",
            thickness=15,
            len=1,
            title_font_size=15,
            tickfont_size=10,
        )
    )

    return fig


def map_abortion_laws():
    """
    Creates a chloropleth map by state of statutory limits on abortion

    Inputs: none
    Outputs: plotly figure

    """
    df = load_data(ABORTION_LAWS, True)

    fig = px.choropleth(
        locations="Abbreviation",
        locationmode="USA-states",
        scope="usa",
        color="Statutory Limit on Abortions",
        custom_data=["Location", "Statutory Limit on Abortions"],
        color_discrete_sequence=[  # pink to dark purple
            "#FFC0CB",
            "#F89AC1",
            "#F472B6",
            "#E847AE",
            "#C44EC1",
            "#9D41C9",
            "#732D91",
            "#4B0082",
        ],
        title="Statutory limit on abortions by state",
        data_frame=df,
    )

    fig.update_traces(
        hovertemplate="<b>State:</b> %{customdata[0]}<br><b>Limit:</b> %{customdata[1]}<extra></extra>"
    )

    return fig


def scatter_mortality_stats(xaxis):
    """
    Creates a scatter plot filtered by state of mortality and other characterists

    Inputs: xaxis specifications for graph
    Outputs: plotly scatter plot

    """

    df = load_data(MERGED, False).dropna()
    df[xaxis] = df[xaxis].astype(float)

    # manually creating trend line with statsmodel package
    model = sm.OLS(df["Maternal Mortality Rate per 100,000 Live Births"], 
                   sm.add_constant(df[xaxis])).fit()
    
    df["trend"] = model.predict(sm.add_constant(df[xaxis]))

    fig = px.scatter(
        data_frame=df,
        x=xaxis,
        y="Maternal Mortality Rate per 100,000 Live Births",
        color="State",
        title=f"Maternal Mortality by {xaxis}",
    )

    fig.add_traces(
        px.line(df, x=xaxis, y="trend").data[0] # adding trend line
    )

    fig.update_traces(marker=dict(size=10))  # make markers bigger

    return fig


def run_app():
    """
    Using dash, display maps, table
    """

    app = Dash()
    app.layout = html.Div(
        [
            # header
            html.Div(
                style={"position": "relative", "textAlign": "center"},
                children=[
                    # Background image
                    html.Img(
                        src="assets/banner_multiple.png",
                        style={"width": "100%", "height": "auto"},
                    ),
                    # Left text
                    html.H3(
                        [
                            "Women in STEM",
                            html.Br(),
                            "CAPP 30122 Project",
                            html.Br(),
                            "Winter 2025",
                        ],
                        style={
                            "position": "absolute",
                            "top": "5%",
                            "left": "5%",
                            "color": "black",
                            "textAlign": "left",
                            "fontFamily": "Arial, sans-serif",
                        },
                    ),
                    # Right text
                    html.H3(
                        [
                            "Click below to see the",
                            html.Br(),
                            html.A(
                                "GitHub repository",
                                href="https://github.com/uchicago-2025-capp30122/30122-project-women-in-stem",
                                target="_blank",
                            ),
                        ],
                        style={
                            "position": "absolute",
                            "top": "5%",
                            "right": "5%",
                            "color": "black",
                            "fontFamily": "Arial, sans-serif",
                        },
                    ),
                ],
            ),
            # Heading, selectors
            html.H1(
                "Analysis of Maternal Mortality Rates and Abortion Legislation",
                style={
                    "textAlign": "center",
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": "32px",
                    "textDecoration": "underline",
                },
            ),
            html.P(
                "Please select the map and data you would like to view",
                style={
                    "fontWeight": "bold",
                    "marginBottom": "15px",
                    "fontFamily": "Arial, sans-serif",
                },
            ),
            dcc.RadioItems(
                options=["Maternal Mortality Rates", "Statutory Limits on Abortion"],
                value="Maternal Mortality Rates",
                id="map_select",
            ),
            html.I(
                "Note: missing mortality rate data for 13 states",
                style={
                    "fontFamily": "Arial, sans-serif",
                    "color": "gray",
                    "fontSize": "13px",
                    "marginBottom": "20px",
                    "marginTop": "10px",
                },
            ),
            # Map and table
            html.Div(
                [
                    dcc.Graph(
                        figure={}, id="map", style={"flex": "1", "maxWidth": "800px"}
                    ),
                    dash_table.DataTable(
                        data=[],
                        page_size=10,
                        id="table",
                        style_table={"flex": "1", "overflowX": "auto"},
                        style_cell={"textAlign": "center"},
                    ),
                ],
                style={"maxWidth": "1200px", "display": "flex", "gap": "20px"},
            ),
            # Scatter plot
            html.Hr(),
            html.P(
                "Please select the x-axis you would like to visualize.",
                style={
                    "fontWeight": "bold",
                    "fontFamily": "Arial, sans-serif",
                    "marginBottom": "15px",
                },
            ),
            dcc.RadioItems(
                options=[
                    "Percent Uninsured",
                    "Women's Average Weekly Earnings",
                    "Ratio of Women's Earnings to Men's Earnings",
                    "Percent Cesarean Births",
                ],
                value="Percent Uninsured",
                id="scatter_select",
            ),
            dcc.Graph(figure={}, id="scatter"),
            html.I(
                "Note: mortality data is from 2018-2021, while earnings data and cesarean data is for the year 2021 and insurance coverage data 2023.",
                style={
                    "fontFamily": "Arial, sans-serif",
                    "color": "gray",
                    "fontSize": "13px",
                    "marginBottom": "20px",
                    "marginTop": "10px",
                },
            ),
        ],
        style={
            "background": "linear-gradient(to right, #fabae2, #f0f8ff)",  # gradient background
            "height": "auto",
            "padding": "20px",
        },
    )

    @callback(  # updating map according to selection
        Output(component_id="map", component_property="figure"),
        Input(component_id="map_select", component_property="value"),
    )
    def update_map(map):
        if map == "Maternal Mortality Rates":
            return map_mortalities()
        return map_abortion_laws()

    @callback(  # updating table according to selection
        Output(component_id="table", component_property="data"),
        Input(component_id="map_select", component_property="value"),
    )
    def update_table(data):
        if data == "Maternal Mortality Rates":
            return (
                load_data(MERGED, False)
                .drop(
                    columns=[
                        "Percent Uninsured",
                        "Women's Average Weekly Earnings",
                        "Ratio of Women's Earnings to Men's Earnings",
                        "Percent Cesarean Births",
                        "Abbreviation",
                    ]
                )
                .to_dict("records")
            )
        return (
            load_data(ABORTION_LAWS, True)
            .drop(columns=["Abbreviation"])
            .to_dict("records")
        )

    @callback(  # updating scatter plot according to selection
        Output(component_id="scatter", component_property="figure"),
        Input(component_id="scatter_select", component_property="value"),
    )
    def update_scatter(data):
        if data == "Percent Uninsured":
            return scatter_mortality_stats("Percent Uninsured")
        elif data == "Women's Average Weekly Earnings":
            return scatter_mortality_stats("Women's Average Weekly Earnings")
        elif data == "Ratio of Women's Earnings to Men's Earnings":
            return scatter_mortality_stats(
                "Ratio of Women's Earnings to Men's Earnings"
            )
        elif data == "Percent Cesarean Births":
            return scatter_mortality_stats("Percent Cesarean Births")

    app.run_server(debug=True, use_reloader=False)


if __name__ == "__main__":
    run_app()
