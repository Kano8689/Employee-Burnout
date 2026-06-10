import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

print("Generating dataset...")
np.random.seed(42)
data_size = 1000
data = {
    'Work_Hours': np.random.randint(4, 14, data_size),
    'Mental_Fatigue_Score': np.random.uniform(0, 10, data_size),
    'Resource_Allocation': np.random.uniform(0, 10, data_size),
    'WFH_Setup_Available': np.random.randint(0, 2, data_size),
    'Designation': np.random.randint(0, 5, data_size)
}
df = pd.DataFrame(data)

df['Burnout_Rate'] = (
    (df['Work_Hours'] / 14) * 0.3 + 
    (df['Mental_Fatigue_Score'] / 10) * 0.4 - 
    (df['Resource_Allocation'] / 10) * 0.15 - 
    (df['WFH_Setup_Available'] * 0.05) + 
    (df['Designation'] / 5) * 0.1 + 
    np.random.normal(0, 0.05, data_size)
).clip(0, 1)

df.to_csv('employee_data.csv', index=False)

print("Training AI Model...")
X = df.drop('Burnout_Rate', axis=1)
y = df['Burnout_Rate']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

print("Saving model and feature impacts...")
joblib.dump(model, 'burnout_model.pkl')

importances = model.feature_importances_
feature_impact = {feature: round(imp * 100, 2) for feature, imp in zip(X.columns, importances)}
joblib.dump(feature_impact, 'feature_impact.pkl')

print("Success! 'burnout_model.pkl' and 'feature_impact.pkl' have been created.")