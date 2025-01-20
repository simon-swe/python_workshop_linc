import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from data_cleaning import findSignificantCategories


# 1) Load data

df = pd.read_excel('credit_card_customers.xlsx')


sig = findSignificantCategories()


significant_columns = [item[0] for item in sig]


significant_cols_info = findSignificantCategories()
significant_cols = [col_info[0] for col_info in significant_cols_info]

df['Churn'] = df['Attrition_Flag'].apply(
    lambda x: 1 if x == 'Attrited Customer' else 0)
df.drop('Attrition_Flag', axis=1, inplace=True)

final_feature_list = significant_cols.copy()
if 'Churn' not in final_feature_list:
    final_feature_list.append('Churn')

df_significant = df[final_feature_list]

X = df_significant.drop('Churn', axis=1)
y = df_significant['Churn']


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
