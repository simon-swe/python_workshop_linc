import pandas as pd
import plotly.express as px
from dash import dash_table
from scipy.stats import chi2_contingency, f_oneway

# Load dataset
df = pd.read_excel('credit_card_customers.xlsx')
classificationCategories = ['Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']
numericalCategories = [
    'Months_on_book', 'Total_Relationship_Count', 'Months_Inactive_12_mon',
    'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
    'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
    'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'
]

# Return the significant categories after filtering using correlation, ANOVA, and Chi-square
def findSignificantCategories():
    chi2Significance = []
    anovaSignificance = []
    reference = 'Attrition_Flag'
    correlation_matrix = df[numericalCategories].corr()
    threshold = 0.8
    high_corr_pairs = [
        (var1, var2) for var1 in correlation_matrix.columns for var2 in correlation_matrix.columns
        if var1 != var2 and abs(correlation_matrix[var1][var2]) > threshold
    ]

    # Keep only one variable from pairs
    variables_to_remove = {pair[1] for pair in high_corr_pairs}
    reducedNumericalCategories = [var for var in numericalCategories if var not in variables_to_remove]

    for i in classificationCategories:
        contingency_table = pd.crosstab(df[reference], df[i])
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        chi2Significance.append([i, p, chi2, dof])

    for i in reducedNumericalCategories:
        grouped_data = [df[df[reference] == group][i] for group in df[reference].unique()]
        f_stat, p_value = f_oneway(*grouped_data)
        anovaSignificance.append([i, p_value, f_stat])

    categoriesSignificance = chi2Significance + anovaSignificance

    isCategorieSignificant = lambda result: result[1] < 0.05

    significantCategories = list(filter(isCategorieSignificant, categoriesSignificance))

    return significantCategories


def getSignificantTables():
    sigCat = findSignificantCategories()

    # Convert significant categories into a DataFrame for Dash DataTable
    data = [{"Variable": row[0], "p-value": row[1]} for row in sigCat]
    table = dash_table.DataTable(
        columns=[
            {"name": "Variable", "id": "Variable"},
            {"name": "p-value", "id": "p-value"},
        ],
        data=data,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '5px',
            'fontSize': '14px',
        },
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': 'lightgrey',
        },
    )
    return table

# Return heatmap with correlation between numerical categories
def getCorrelationHeatmap():
    correlation_matrix = df[numericalCategories].corr()

    corr_melted = correlation_matrix.reset_index().melt(
        id_vars='index',
        var_name='Feature_2',
        value_name='Correlation'
    )
    corr_melted.rename(columns={'index': 'Feature_1'}, inplace=True)

    heatmap = px.imshow(
        correlation_matrix,
        labels=dict(x="Features", y="Features", color="Correlation"),
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
    )
    heatmap.update_layout(
        title="Correlation Matrix Heatmap",
        width=800,
        height=800
    )
    return heatmap
