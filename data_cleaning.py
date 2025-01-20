import pandas as pd
from scipy.stats import chi2_contingency, f_oneway

# Load the dataset
df = pd.read_excel('credit_card_customers.xlsx')


def findSignificantCategories():
    chi2Significance = []
    anovaSignificance = []

    reference = 'Attrition_Flag'
    classificationCategories = ['Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category']
    numericalCategories = [
        'Months_on_book', 'Total_Relationship_Count', 'Months_Inactive_12_mon',
        'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal',
        'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
        'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'
    ]

    # Perform Chi-Square Test for categorical variables
    for i in classificationCategories:
        contingency_table = pd.crosstab(df[reference], df[i])
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        chi2Significance.append([i, p, chi2, dof])

    # Perform ANOVA Test for numerical variables
    for i in numericalCategories:
        grouped_data = [df[df[reference] == group][i] for group in df[reference].unique()]
        f_stat, p_value = f_oneway(*grouped_data)
        anovaSignificance.append([i, p_value, f_stat])

    # Combine significant results
    categoriesSignificance = chi2Significance + anovaSignificance

    # Filter significant categories based on a threshold
    isCategorieSignificant = lambda result: result[1] < 0.05

    significantCategories = list(filter(isCategorieSignificant, categoriesSignificance))

    # Remove highly correlated numerical variables
    correlation_matrix = df[numericalCategories].corr()
    threshold = 0.8

    # Find pairs of highly correlated variables
    high_corr_pairs = [
        (var1, var2) for var1 in correlation_matrix.columns for var2 in correlation_matrix.columns
        if var1 != var2 and abs(correlation_matrix[var1][var2]) > threshold
    ]
    print("Highly correlated pairs:", high_corr_pairs)

    # Keep only one variable from each highly correlated pair
    variables_to_remove = {pair[1] for pair in high_corr_pairs}
    reducedNumericalCategories = [var for var in numericalCategories if var not in variables_to_remove]

    # Add p-value and F-statistic to variable names
    numericalStats = {result[0]: (result[1], result[2]) for result in anovaSignificance}
    reducedNumericalCategoriesWithStats = [
        f"{var} (p={numericalStats[var][0]:.4f}, F={numericalStats[var][1]:.2f})"
        for var in reducedNumericalCategories
    ]

    return significantCategories, reducedNumericalCategoriesWithStats, high_corr_pairs

ret = findSignificantCategories()
print()
