"""
This script is designed to create linear regression model that help user
estimate/predict the maternal mortality rate given different factors/characterisitcs
"""

from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

# independent variable of interest
INDEPENDENT_VAR = ["region", "race", "education", "ten_year_age_groups"]


def get_data():
    """
    Retrieved the cleaned data for crearing visualization and randomly split them
    into training and testing data

    Returns:
        mortality_data (DataFrame): the entire cleaned data
    """
    file = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
    mortality_data = pd.read_csv(file)
    mortality_data = mortality_data[
        mortality_data["race"] != "American Indian or Alaska Native"
    ]

    return mortality_data


def full_model(mortality_data):
    """
    Create the optimal linear regression model with all data available

    Parameters:
        mortality_data (Dataframe): Dataframe containing all variables data

    Returns:
        predict_model: linear regression of all variables maternal mortality
    """
    equation_str = "mortality_binary ~ " + "+".join(INDEPENDENT_VAR)
    train_model = smf.logit(equation_str, data=mortality_data).fit()

    return train_model, train_model.prsquared


def user_prediction(
    region: str = "northeast",
    race: str = "white",
    education: str = "unknown",
    age: str = "15-24",
):
    """
    Generate the predicted maternal mortality rate from the linear regression
    model based on user input as well as shown model equation

    Parameters:
        Region of User Input (str)
        Race of User Input (str)
        Education of User Input (str)
        Age of User Input (str)

    Returns:
        Maternal mortality rate (float)
    """
    mortality_data = get_data()

    full_logit_model, _ = full_model(mortality_data)
    print(full_logit_model.summary())

    inputs = pd.DataFrame(
        {
            INDEPENDENT_VAR[0]: [region],
            INDEPENDENT_VAR[1]: [race],
            INDEPENDENT_VAR[2]: [education],
            INDEPENDENT_VAR[3]: [age],
        }
    )

    user_mortality_r = full_logit_model.predict(inputs)

    # return user_mortality_r.values[0]
    return round(user_mortality_r.values[0], 3)


def user_input_dash():
    """
    Create Dash Interaction in the web browser consists of two components:
    the predictive model and the data visualization. Both components will show
    the output once user make selections

    Paremeters:
        None

    Returns:
        None
    """
    mortalty_data = get_data()

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
                            #'fontFamily': 'Arial, sans-serif'
                            #'font-style': 'italic'
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
                            #'fontFamily': 'Arial, sans-serif'
                            #'font-style': 'italic'
                        },
                    ),
                ],
            ),
            # first component (predictive model)
            html.H1(
                "Predictive Model of Maternal Mortality Rate",
                style={
                    "textAlign": "center",
                    "fontFamily": "Arial, sans-serif",
                    "text-decoration": "underline",
                    "margin-bottom": "2px",
                },
            ),
            html.H2(
                "Based on Region, Race, Education, and Age",
                style={
                    "textAlign": "center",
                    "fontFamily": "Arial, sans-serif",
                    "font-style": "italic",
                    "margin-top": "2px",
                },
            ),
            html.I(
                "Choose the following characteristics that most describe you. Note that all options are based on the CDC WONDER online database.",
                style={
                    "textAlign": "left",
                    "fontFamily": "Arial, sans-serif",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "marginBottom": "20px",
                    "color": "gray",
                },
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        sorted(mortalty_data["region"].unique()),
                        placeholder="Select Region...",
                        id="region",
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        sorted(mortalty_data["race"].unique()),
                        placeholder="Select Race...",
                        id="race",
                    )
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        mortalty_data["education"].unique(),
                        placeholder="Select Education Level...",
                        id="education",
                    )
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        sorted(mortalty_data["ten_year_age_groups"].unique()),
                        placeholder="Select Age Group...",
                        id="age",
                    )
                ]
            ),
            html.Div(
                id="header-mortality",
                style={
                    "textAlign": "left",
                    "fontFamily": "Arial, sans-serif",
                    "marginTop": "20px",
                    "marginBottom": "5px",
                    "textDecoration": "underline",
                },
            ),
            html.Div(id="output-mortality", style={"marginBottom": "20px"}),
            html.Div(id="explain-mortality", style={"marginBottom": "20px"}),
            # second component (visualization)
            html.H2(
                [
                    html.Br(),
                    "How might different charactersitics be correlated to maternal mortality?",
                ],
                style={
                    "textAlign": "left",
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": "20px",
                    "marginTop": "20px",
                    "marginBottom": "2px",
                },
            ),
            html.I(
                "Choose up to two characteristics below to visualize how they relate to maternal mortality.",
                style={
                    "textAlign": "left",
                    "fontFamily": "Arial, sans-serif",
                    "fontWeight": "bold",
                    "fontSize": "16px",
                    "marginBottom": "20px",
                    "color": "gray",
                },
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        INDEPENDENT_VAR,
                        placeholder="Select Variable of Interest",
                        id="indepdent-var1",
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        INDEPENDENT_VAR,
                        placeholder="Select Variable of Interest",
                        id="indepdent-var2",
                    ),
                ]
            ),
            dcc.Graph(id="boxplot"),
        ],
        style={
            "background": "linear-gradient(to right, #fabae2, #f0f8ff)",  # gradient background
            "height": "auto",
            "padding": "7px",
        },
    )

    # create the predicted mortality rate based on user inputs
    @callback(
        Output(component_id="header-mortality", component_property="children"),
        Output(component_id="output-mortality", component_property="children"),
        Output(component_id="explain-mortality", component_property="children"),
        [
            Input(component_id="region", component_property="value"),
            Input(component_id="race", component_property="value"),
            Input(component_id="education", component_property="value"),
            Input(component_id="age", component_property="value"),
        ],
    )
    def output_mortality_rate(region, race, education, age):
        if None in [region, race, education, age]:
            return "", "", ""

        predicted_result = user_prediction(region, race, education, age)
        explanation = f"This predicted value tells us there is a {round(predicted_result * 100, 1)}% probability of your mortality rate being high. In this analysis, a threshold of 1% is used to distinguish between a low maternal mortality rate and a high maternal mortality rate, where 1% means that out of 100 live births, there was 1 maternal death. The 'low' maternal mortaity rate ranges from 0% to 1%, and a 'high' maternal mortality rate ranges from 1% to 5.5%."
        return (
            "The prediction analysis",
            f"Based on the given characteristics, your predicted value is {predicted_result}.",
            explanation,
        )

    # create data expldoration visulization based on user inputs
    @callback(
        Output(component_id="boxplot", component_property="figure"),
        Input(component_id="indepdent-var1", component_property="value"),
        Input(component_id="indepdent-var2", component_property="value"),
    )
    def update_boxplot(independent_var1, independent_var2):
        fig = px.box(
            mortalty_data,
            x=independent_var1,
            y="mortality_rate",
            color=independent_var2,
        )
        fig.update_layout(
            title={"text": "Box Plot of Maternal Mortality Rates", "x": 0.5},
            yaxis_title="Maternal Mortality Rates",
        )

        return fig

    app.run_server(debug=True)


if __name__ == "__main__":
    user_input_dash()
