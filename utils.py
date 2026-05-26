import os
import pandas as pd
from flask import request  
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Global variable to hold our trained model instance
model = None

def train_burnout_model():
    """
    Loads data and trains the Decision Tree model once when the app boots up.
    """
    global model
    
    dataset_path = "Datasets/employee_burnout.csv"
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Could not find the dataset at {dataset_path}")
        
    df = pd.read_csv(dataset_path)

    # Clean and standardize column references
    df = df.rename(columns={
        'Gender': 'Gender',
        'Company Type': 'Company_Type',
        'WFH Setup Available': 'WFH_Setup_Available',
        'Designation': 'Designation',
        'Resource Allocation': 'Resource_Allocation',
        'Mental Fatigue Score': 'Mental_Fatigue_Score',
        'Burn Rate': 'Burn_Rate'
    })

    df = df.drop(["Employee ID", "Date of Joining"], axis=1, errors='ignore')
    df = df.dropna()

    # Convert continuous target into category classifications
    def burnout_category(rate):
        if rate <= 0.3: return "Low"
        elif rate <= 0.6: return "Medium"
        else: return "High"

    df["Burnout_Level"] = df["Burn_Rate"].apply(burnout_category)
    df = df.drop("Burn_Rate", axis=1)

    # Explicit mapping used here instead of dynamic LabelEncoder fit loops.
    # Alphabetical sorting mapping: Female=0/Male=1, Product=0/Service=1, No=0/Yes=1
    # For target: High=0, Low=1, Medium=2
    df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})
    df['Company_Type'] = df['Company_Type'].map({'Product': 0, 'Service': 1})
    df['WFH_Setup_Available'] = df['WFH_Setup_Available'].map({'No': 0, 'Yes': 1})
    df['Burnout_Level'] = df['Burnout_Level'].map({'High': 0, 'Low': 1, 'Medium': 2})
    
    # Fill any parsing mismatches safely
    df = df.dropna()

    X = df.drop("Burnout_Level", axis=1)
    y = df["Burnout_Level"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    print("Decision Tree Model successfully trained and ready.")


def calculate_form_burnout():
    """
    Extracts HTTP POST data from the active Flask request scope,
    runs the ML model prediction, and evaluates a gauge float return value.
    """
    global model
    if model is None:
        train_burnout_model()

    # 1. Capture user inputs directly from the active Flask form request context
    gender = request.form.get('gender', 'Male')
    company_type = request.form.get('company_type', 'Service')
    wfh_setup = request.form.get('wfh_setup', 'No')
    designation = int(request.form.get('designation', 1))
    resource_allocation = float(request.form.get('resource_allocation', 1.0))
    mental_fatigue = float(request.form.get('mental_fatigue', 0.0))

    # 2. Replicate the precise encoding indices learned by the model
    gender_encoded = 1 if gender.lower() == "male" else 0
    company_encoded = 1 if company_type.lower() == "service" else 0
    wfh_encoded = 1 if wfh_setup.lower() == "yes" else 0

    # 3. Build a single-row matrix DataFrame matching structural training dependencies
    user_data = pd.DataFrame([[
        gender_encoded,
        company_encoded,
        wfh_encoded,
        designation,
        resource_allocation,
        mental_fatigue
    ]], columns=['Gender', 'Company_Type', 'WFH_Setup_Available', 'Designation', 'Resource_Allocation', 'Mental_Fatigue_Score'])

    # 4. Generate model prediction label index (0, 1, or 2)
    prediction_class = int(model.predict(user_data)[0])

    # 5. Map classifications to mid-segment positions on the frontend speedometer (0.0 to 1.0 scale)
    # High (Class 0) -> 0.85, Low (Class 1) -> 0.15, Medium (Class 2) -> 0.45
    gauge_mapping = {
        0: 0.85,  
        1: 0.15,  
        2: 0.45   
    }

    return gauge_mapping.get(prediction_class, 0.0)