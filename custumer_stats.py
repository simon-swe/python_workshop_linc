import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#returns general stats comparing attrition flag and different categories
def getCustumerStats():
    plots = [];
    df = pd.read_excel('credit_card_customers.xlsx')
    sns.countplot(x='Attrition_Flag', 
                  data=df, 
                  order=df['Attrition_Flag'].value_counts().index)
    plt.title("Distribution of Attrition Flag (Attrited vs. Existing Customers)")
    plt.xlabel("Attrition Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plots.append(plt.gcf())
    plt.show()
    
    features_of_interest = ['Gender', 'Marital_Status', 'Income_Category',
                            'Months_on_book', 'Education_Level']
    
    df_left = df[df['Attrition_Flag'] == 'Attrited Customer']
    for feature in features_of_interest:
        print(f"\nDistribution of {feature} for clients who left:")
        print(df_left[feature].value_counts(dropna=False, normalize=True))

        plt.figure(figsize=(4, 3))
        sns.countplot(x=feature, data=df_left,
                    order=df_left[feature].value_counts().index)
        plt.title(f"Distribution of {feature} (Closed Accounts)")
        plt.tight_layout()
        plots.append(plt.gcf())
        plt.show()

    return plots
ret = getCustumerStats()
print()