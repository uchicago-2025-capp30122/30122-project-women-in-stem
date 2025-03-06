"""
This script is designed to create linear regression model that help user
estimate/predict the maternal mortality rate given different factors/characterisitcs
"""

from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
import numpy as np

# from rich.console import Console
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score
# from sklearn.linear_model import LogisticRegression
from dash import Dash, dcc, html, Input, Output,callback
import plotly.express as px


INDEPENDENT_VAR = ['region', 'race','education', 'ten_year_age_groups']

def get_data():
    """
    Retrieved the cleaned data for crearing visualization and randomly split them
    into training and testing data

    Returns:
        mortality_data (DataFrame): the entire cleaned data
    """
    file = Path(__file__).parent.parent.joinpath("data/clean_reg_age_educ.csv")
    mortality_data = pd.read_csv(file)
    mortality_data = mortality_data[mortality_data['race'] != "american indian or alaska native"]
    mortality_data['mortality_rate'] = mortality_data['percent_total_deaths']/100
    median_mortal = mortality_data['mortality_rate'] .median()
    # mortality_data['mortality_binary'] = (mortality_data['mortality_rate'] > median_mortal).astype(int)
    print(mortality_data['mortality_rate'].unique())
    mortality_data['mortality_binary'] = (mortality_data['mortality_rate'] > 0.01).astype(int)
    # train_data, test_data = train_test_split(mortality_data, test_size = 0.2, random_state = 100)

    # return train_data, test_data
    return mortality_data

def full_model(mortality_data):
# def full_model(train_data, test_data):
    """
    Create the optimal linear regression model with all data available

    Parameters:
        mortality_data (Dataframe): Dataframe containing all variables data

    Returns:
        predict_model: linear regression of all variables maternal mortality
    """

    # equation_str = "percent_total_deaths ~ " + "+".join(INDEPENDENT_VAR)
    # equation_str = "mortality_rate ~ " + "+".join(INDEPENDENT_VAR)
    # train_model = smf.ols(equation_str, data=mortality_data).fit()
    equation_str = "mortality_binary ~ " + "+".join(INDEPENDENT_VAR)
    print('eq', equation_str)
    train_model = smf.logit(equation_str, data=mortality_data).fit()
    # train_model = train_model.fit()
    # maternal_predicted = train_model.predict(exog = test_data)
    # test_r2 = r2_score(test_data['percent_total_deaths'], maternal_predicted)

    # print(train_model.summary())
    # print('r^2',test_r2)
    
    # return equation_str, train_model, test_r2
    # return train_model
    # return train_model, train_model.rsquared
    return train_model, train_model.prsquared

def user_prediction(region:str, race:str, education:str, age:str):
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
    # train_data, test_data = get_data()
    mortality_data = get_data()
    # print(mortality_data['mortality_rate'].unique())
    # optimal_equation, opt_model = optimal_model(train_data, test_data)

    full_logit_model, _ = full_model(mortality_data)
    # full_logit_model = full_model(mortality_data)
    print(full_logit_model.summary())
    # print(logit_r2)
    # console = Console()


    inputs = pd.DataFrame({
        INDEPENDENT_VAR[0] : [region],
        INDEPENDENT_VAR[1] : [race],
        INDEPENDENT_VAR[2] : [education],
        INDEPENDENT_VAR[3] : [age]
    })
    
    # user_mortality_r = opt_model.predict(inputs)
    # console.print(user_mortality_r)
    # console.print("predictive model:", complete_equation)
    user_mortality_r = full_logit_model.predict(inputs)
    return user_mortality_r

def user_input_dash():
    mortalty_data = get_data()
    # print('data', mortalty_data)
    app = Dash()
    app.layout = html.Div([
        html.H1("Predictive Model of Maternal Mortality Rate on State Region, Race, Education, and Age (ten-year based)", style={'textAlign': 'left', 'fontSize': '32px', 'textDecoration': 'underline'}),

        html.I("Please choose the following characteristics that most describe you. Please note that all options are based on CDC Wonder online database", style={'fontWeight': 'bold', 'marginBottom': '20px'}),
        html.Div([
            dcc.Dropdown(mortalty_data['region'].unique(), placeholder="Select State Region...", id='region'),
        ]),
        html.Div([
            dcc.Dropdown(mortalty_data['race'].unique(), placeholder="Select Race...", id='race')
        ]),
        html.Div([
            dcc.Dropdown(mortalty_data['education'].unique(), placeholder="Select Education Level", id='education')
        ]),
        html.Div([
            dcc.Dropdown(sorted(mortalty_data['ten_year_age_groups'].unique()), placeholder="Select Age Group", id='age',style={'marginBottom': '20px'})
        ]),

        # html.H2("Your predicted maternal mortality rate Analysis", style={'textDecoration': 'underline'}),
        html.Div(id='header-mortality', style={'textAlign': 'left', 'marginBottom': '20px', 'textDecoration': 'underline'}),
        html.Div(id='output-mortality', style={'marginBottom': '20px'}),
        # dcc.Graph(id='indicator-graphic')
        # html.Div(id='explain-mortality', style={'marginBottom': '20px'})
        html.H2("How different charactersitics may correlated to Maternal Mortality?", style={'textAlign': 'left', 'fontSize': '32px', 'textDecoration': 'underline'}),

    ])

    @callback(
        Output(component_id = 'header-mortality', component_property = 'children'),
        Output(component_id = 'output-mortality', component_property = 'children'),
        Input(component_id='region', component_property = 'value'),
        Input(component_id='race', component_property = 'value'),
        Input(component_id='education', component_property = 'value'),
        Input(component_id='age', component_property = 'value'),
    )

    def output_mortality_rate(region, race, education, age):
        predicted_result = user_prediction(region, race, education, age)
        predicted_value = predicted_result.values[0]
        print(predicted_result)
        # header = f"your prediction analysis"
        # print('your prediction analysis')
        if pd.isna(predicted_value):
            predicted_value = "..."
        else:
            return "The prediction analysis", f"Based on the given characteristics, your predicted maternal mortality is {predicted_value}"

    # @callback(
    #     Output(component_id = 'output-mortality', component_property = 'value'),
    #     Input(component_id = 'output-mortality', component_property = 'children')

    # )

    # def explain_mortality(mortality_rate):
    #     print('mortal', type(mortality_rate))
    #     split_word = mortality_rate.split()
    #     actual_mortal = split_word[-1]
    #     return f"Out of 100 women that live in the same and has the same charactersics, {actual_mortal} people would die form maternal mortality"
    
    app.run_server(debug=True)

if __name__ == '__main__':
    user_input_dash()