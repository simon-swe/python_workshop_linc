import pandas as pd
import plotly.express as px


def getCustomerStats():
    plots = []

    df = pd.read_excel('credit_card_customers.xlsx')

    fig1 = px.histogram(df, x='Attrition_Flag')
    fig1.update_layout(
        title="Distribution of Attrition Flag (Attrited vs. Existing Customers)",
        xaxis_title="Attrition Status",
        yaxis_title="Count",
        bargap=0.2
    )
    plots.append(fig1)
    df_left = df[df['Attrition_Flag'] == 'Attrited Customer']

    features_of_interest = ['Gender', 'Marital_Status', 'Income_Category',
                            'Months_on_book', 'Education_Level']

    for feature in features_of_interest:
        print(f"\nDistribution of {feature} for clients who left:")
        print(df_left[feature].value_counts(dropna=False, normalize=True))

        fig = px.histogram(
            df_left.sort_values(by=feature),
            x=feature,
        )
        fig.update_layout(
            title=f"Distribution of {feature} (Attrited/Closed Accounts)",
            xaxis_title=feature,
            yaxis_title="Count"
        )
        plots.append(fig)
    return plots
