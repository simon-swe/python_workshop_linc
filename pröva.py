import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from customFunctions import isCategorieSignificant
from data_cleaning import findSignificantCategories

# 1. Load the dataset
df = pd.read_excel('credit_card_customers.xlsx')

df['Gender'] = df['Gender'].map({'F': 0, 'M': 1})
df['Income_Category'] = df['Income_Category'].map({'Less than $40K': 0,
                                                   '$40K - $60K': 1,
                                                   '$60K - $80K': 2,
                                                   '$80K - $120K': 3,
                                                   '$120K +': 4,
                                                   'Unknown': 5})

# 2. Define / Run findSignificantCategories (already in your code)

# 3. Get the significant columns
significant_cols_info = findSignificantCategories()
significant_cols = [col_info[0] for col_info in significant_cols_info]

# 4. Create numeric churn column
df['Churn'] = df['Attrition_Flag'].apply(
    lambda x: 1 if x == 'Attrited Customer' else 0)
df.drop('Attrition_Flag', axis=1, inplace=True)

# 5. Subset the DataFrame with the significant columns + 'Churn'
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


# 8. Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_prob = rf.predict_proba(X_test)[:, 1]


# threshold = 0.1 A lower threshold identifies more of the churn customers but also guesses wrong more ofter
threshold = 0.5
y_pred = (y_prob >= threshold).astype(int)


#y_pred = rf.predict(X_test)

print("==== Random Forest Results ====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# 9. (Optional) Feature Importances
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = np.argsort(importances)[::-1]

print("\n=== FEATURE IMPORTANCES ===")
for idx in sorted_idx:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")
