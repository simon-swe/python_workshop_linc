import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getCustumerStats():
    plots = [];
    # 1. Load the dataset
    df = pd.read_excel('credit_card_customers.xlsx')
    # Adjust the path/filename as necessary

    # 2. Basic look at dataset shape and columns
    print("Dataset shape:", df.shape)
    print("Columns:", df.columns)

    # 3. Proportion of clients who have left vs. stayed
    print("\nProportion of clients (Attrition_Flag):")
    print(df['Attrition_Flag'].value_counts())

    sns.countplot(
    x='Attrition_Flag', 
    data=df,  # Ensure the DataFrame is correctly defined
    order=df['Attrition_Flag'].value_counts().index)
    plt.title("Distribution of Attrition Flag (Attrited vs. Existing Customers)")
    plt.xlabel("Attrition Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
    
    # 5. Distribution of selected features among those who left
    #    Here we show examples for Gender, Marital_Status, Income_Category, Months_on_book, Education_Level
    #    Adjust names as they appear in your dataset.
    features_of_interest = ['Gender', 'Marital_Status', 'Income_Category',
                            'Months_on_book', 'Education_Level']
    
    df_left = df[df['Attrition_Flag'] == 'Attrited Customer']
    for feature in features_of_interest:
        print(f"\nDistribution of {feature} for clients who left:")
        print(df_left[feature].value_counts(dropna=False, normalize=True))

        # OPTIONAL: quick bar plot for each feature
        plt.figure(figsize=(4, 3))
        sns.countplot(x=feature, data=df_left,
                    order=df_left[feature].value_counts().index)
        plt.title(f"Distribution of {feature} (Closed Accounts)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # 6. (Optional) Basic numeric summaries (e.g. describing numerical columns)
    print("\nStatistical summary of numerical columns (for those who left):")
    print(df_left.describe())
ret = getCustumerStats()
print()