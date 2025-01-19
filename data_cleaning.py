import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import pandas as pd
from scipy.stats import f_oneway
from customFunctions import *
# 1. Load the dataset
df = pd.read_excel('credit_card_customers.xlsx')

def findSignificantCategories():
    chi2Significance = []
    anovaSignificance = []

    reference = 'Attrition_Flag'
    classificationCatagories = ['Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']
    numericalCatagories = ['Months_on_book',
            'Total_Relationship_Count', 'Months_Inactive_12_mon',
            'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
            'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
            'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio']

    for i in classificationCatagories:
        contingency_table = pd.crosstab(df[reference], df[i])
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        chi2Significance.append([i, p, chi2, dof])


    for i in numericalCatagories:
        grouped_data = [df[df[reference] == group][i] for group in df[reference].unique()]
        f_stat, p_value = f_oneway(*grouped_data)
        anovaSignificance.append([i, p_value, f_stat])


    categoriesSignificance  = chi2Significance + anovaSignificance
    significantCategories = list(filter(isCategorieSignificant, categoriesSignificance))
    return significantCategories





