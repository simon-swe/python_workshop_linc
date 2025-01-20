import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# returns general stats comparing attrition flag and different categories


import plotly.express as px


def getCustomerStats():
    plots = []

    # 1) Load Data
    df = pd.read_excel('credit_card_customers.xlsx')

    # 2) Distribution of Attrition Flag (similar to sns.countplot)
    #    Using px.histogram is an easy way to do a "count" of a categorical variable.
    fig1 = px.histogram(df, x='Attrition_Flag')
    fig1.update_layout(
        title="Distribution of Attrition Flag (Attrited vs. Existing Customers)",
        xaxis_title="Attrition Status",
        yaxis_title="Count",
        bargap=0.2  # space between bars, optional
    )
    plots.append(fig1)

    # 3) Subset where customers left (i.e., Attrited)
    df_left = df[df['Attrition_Flag'] == 'Attrited Customer']

    # 4) For each "feature of interest", show distribution among df_left
    features_of_interest = ['Gender', 'Marital_Status', 'Income_Category',
                            'Months_on_book', 'Education_Level']

    for feature in features_of_interest:
        print(f"\nDistribution of {feature} for clients who left:")
        print(df_left[feature].value_counts(dropna=False, normalize=True))

<<<<<<< HEAD
        plt.figure(figsize=(4, 3))
        sns.countplot(x=feature, data=df_left,
                    order=df_left[feature].value_counts().index)
        plt.title(f"Distribution of {feature} (Closed Accounts)")
        plt.tight_layout()
        plots.append(plt.gcf())
        plt.show()
=======
        # Create a histogram or bar chart
        # If the feature is categorical, histogram will create a count by default
        # If it's numeric (like 'Months_on_book'), it creates bins, but that may be okay for quick distribution
        # Alternatively, for numeric, you could set e.g. nbins=15 or so in px.histogram, or use px.bar if appropriate.
        fig = px.histogram(
            df_left,
            x=feature,
            # If numeric, you might also do something like:
            # nbins=10
        )
        fig.update_layout(
            title=f"Distribution of {feature} (Attrited/Closed Accounts)",
            xaxis_title=feature,
            yaxis_title="Count"
        )
        # Rotate x-ticks if needed
        # fig.update_xaxes(tickangle=45)

        plots.append(fig)
>>>>>>> 46b0988e4b669d4755ced2c6b637c2d8c20bf2c2

    return plots


# Example usage:
ret = getCustomerStats()

# Print a newline after the stats
print()

# Optional: if you want to show the figures in a script or notebook:
# for i, fig in enumerate(ret):
#     fig.show()
