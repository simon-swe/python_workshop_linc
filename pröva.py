import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from data_cleaning import findSignificantCategories
import plotly.express as px
from sklearn.metrics import roc_curve, roc_auc_score
import plotly.graph_objs as go

df = pd.read_excel('credit_card_customers.xlsx')

df['Gender'] = df['Gender'].map({'F': 0, 'M': 1})
df['Income_Category'] = df['Income_Category'].map({'Less than $40K': 0,
                                                   '$40K - $60K': 1,
                                                   '$60K - $80K': 2,
                                                   '$80K - $120K': 3,
                                                   '$120K +': 4,
                                                   'Unknown': 5})

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

y_prob = rf.predict_proba(X_test)[:, 1]

threshold = 0.5
y_pred = (y_prob >= threshold).astype(int)

confusionMatrix = confusion_matrix(y_test, y_pred)

print("==== Random Forest Results ====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusionMatrix)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Heatmap


def getConfusion():

    cm = px.imshow(
        confusionMatrix,
        text_auto=True,
        color_continuous_scale="Blues")
    cm.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Label",
        yaxis_title="True Label",
        width=500,
        height=500
    )
    cm.update_xaxes(showticklabels=False)
    cm.update_yaxes(showticklabels=False)
    return cm


importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = np.argsort(importances)[::-1]

print("\n=== FEATURE IMPORTANCES ===")
for idx in sorted_idx:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")


y_probs = rf.predict_proba(X_test)[:, 1]


fpr, tpr, thresholds = roc_curve(y_test, y_probs)
auc_value = roc_auc_score(y_test, y_probs)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC={auc_value:.2f})',
        line=dict(color='blue', width=2)
    )
)

fig.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Random',
        line=dict(color='gray', width=2, dash='dash')
    )
)

fig.update_layout(
    title='ROC Curve for Random Forest',
    xaxis_title='False Positive Rate',
    yaxis_title='True Positive Rate',
    width=600,
    height=500
)


def roc():
    return fig
