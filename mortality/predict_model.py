"""
This script is designed to create linear regression model that help user
estimate/predict the maternal mortality rate given different factors/characterisitcs
"""

import pathlib
import pandas as pd
import statsmodels.formula.api as smf
from rich.console import Console

BASE_DIR = pathlib.Path(__file__).parent.parent

def get_data():
    """
    Retrieved the cleaned data for crearing visualization and randomly split them 
    into training and testing data

    Returns: 
        mortality_data (DataFrame): the entire cleaned data
    """
    mortality_data = pd.read_csv(BASE_DIR/"../data/merged.csv")

    return mortality_data

def level_elimination(columns):
    """
    Compute each level of backward elimination; that is removing one variable
    from the model at a time

    Parameters:
        columns (list): list containing all independent/column variable names

    Returns: 
        inde_list (list): list containing different combination of independent
        variables
    """
    rv = []
    for col in columns:
        p_minus_x = [v for v in col if v!= col]
        rv.append(p_minus_x)
    return rv

def one_level_optimal_model(mortality_data, indep_list):
    """
    Find the optimal linear regression model on specific elimination level which
    is the model with the lowest AIC score

    Parameters:
        mortality_data (Dataframe): Dataframe containing all data
        columns (list): list containing all independent/column variable names

    Returns: 
        indep_list (list): list containing different combination of independent
        variables for optimal model
    """

    #create the full linear regression model 
    equation_str = "mortality_rate ~ "+"+".join(indep_list)
    current_model = smf.ols(equation_str, data= mortality_data).fit()
    lowest_aic = current_model.aic
    new_indep_list = indep_list

    elim_list= level_elimination(indep_list)

    #finding the lowest aic score
    for each_e in elim_list:
        new_equation = "mortality_rate ~ "+"+".join(each_e)
        new_model = smf.ols(new_equation, data= mortality_data).fit()
        if new_model.aic < lowest_aic:
            lowest_aic = new_model.aic
            new_indep_list = each_e

    return new_indep_list

def multi_level_optimal_model(mortality_data, current_indep_list, old_indep_list = []):
    """
    Find the optimal model through the whole process of backward elimination. 
    Stop finding the model when the previous level of elimination is the same as 
    the current level of elimination. In other words, no new model that better 
    fit the data

    Returns:
        list containing different combination of independent variables for 
        multilevel optimal model

    """
    if current_indep_list == old_indep_list:
        return current_indep_list

    newer_list = one_level_optimal_model(mortality_data, indep_list = current_indep_list)

    return multi_level_optimal_model(mortality_data, newer_list, old_indep_list = current_indep_list)


def optimal_predict_model(mortality_data):
    """
    Create linear regression model of maternal mortalitis on the factors of interests.

    Returns:
        predict_model: linear regression of maternal mortality 
    """

    dependent_var = mortality_data.columns()
    equation_str = "mortality_rate ~ "+"+".join(dependent_var)
    predict_model = smf.ols(equation_str, data= mortality_data).fit()

    return predict_model

def user_prediction(mortality_data):
    """
    Generate the predicted maternal mortality rate from the linear regression 
    model based on user input as well as shown model equation

    Returns:
        Maternal mortality rate (float)
    """
    optimal_model = optimal_predict_model(mortality_data)

    # Generate the equation model for view
    console = Console()
    front_equation = "mortality_rate = "
    coeffs = optimal_model.params
    coeff_pairs = []

    for variable, coef in coeffs.items():
        coef = round(coef, 5)
        if variable == 'Intercept':
            coeff_pairs.append(str(coef))
        else:
            coeff_pairs.append(variable+"*"+str(coef))
    
    back_equation = "+".join(coeff_pairs)
    complete_equation = front_equation + back_equation
    console.print("predictive model:", complete_equation)

    # Generate the maternality mortality rate based on user input
    




