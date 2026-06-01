import os
import pandas as pd
from flask import request
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# from sklearn.tree import DecisionTreeClassifier

# Global variable to hold our trained model instance
model = None
feature_importance = {}

def train_burnout_model():
    """
    Loads data and trains the Random Forest model once when the app boots up.
    """
    global model
    global feature_importance

    dataset_path = "Datasets/employee_burnout.csv"

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(
            f"Could not find the dataset at {dataset_path}"
        )

    # Load dataset
    df = pd.read_csv(dataset_path)

    # Rename columns for easier handling
    df = df.rename(columns={
        'Company Type': 'Company_Type',
        'WFH Setup Available': 'WFH_Setup_Available',
        'Resource Allocation': 'Resource_Allocation',
        'Mental Fatigue Score': 'Mental_Fatigue_Score',
        'Burn Rate': 'Burn_Rate'
    })

    # Remove unnecessary columns
    df = df.drop(
        ["Employee ID", "Date of Joining"],
        axis=1,
        errors='ignore'
    )

    # Remove missing values
    df = df.dropna()

    # Encode categorical features
    df['Gender'] = df['Gender'].map({
        'Female': 0,
        'Male': 1
    })

    df['Company_Type'] = df['Company_Type'].map({
        'Product': 0,
        'Service': 1
    })

    df['WFH_Setup_Available'] = df['WFH_Setup_Available'].map({
        'No': 0,
        'Yes': 1
    })

    # Remove rows that failed mapping
    df = df.dropna()

    # Features and target
    X = df.drop("Burn_Rate", axis=1)
    y = df["Burn_Rate"]

    # Train/Test Split
    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train Random Forest
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Store feature importance percentages
    raw_importance = model.feature_importances_

    total = sum(raw_importance)

    feature_importance = {
        feature: round((importance / total) * 100, 2)
        for feature, importance in zip(
            X.columns,
            raw_importance
        )
    }

    print("\n===== FEATURE IMPORTANCE =====")

    for feature, score in sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{feature}: {score}%")

    print("\nRandom Forest Model successfully trained and ready.")


def calculate_form_burnout():
    """
    Extracts HTTP POST data from the active Flask request scope,
    runs the ML model prediction,
    and returns burnout score, feature importance and recommendation.
    """

    global model
    global feature_importance

    if model is None:
        train_burnout_model()

    # Get form values
    gender = request.form.get('gender', 'Male')
    company_type = request.form.get('company_type', 'Service')
    wfh_setup = request.form.get('wfh_setup', 'No')
    designation = int(request.form.get('designation', 1))
    resource_allocation = float(
        request.form.get('resource_allocation', 1)
    )
    mental_fatigue = float(
        request.form.get('mental_fatigue', 0)
    )

    # Encode categorical values
    gender_encoded = 1 if gender == "Male" else 0
    company_encoded = 1 if company_type == "Service" else 0
    wfh_encoded = 1 if wfh_setup == "Yes" else 0

    # Create input dataframe
    user_data = pd.DataFrame([[
        gender_encoded,
        company_encoded,
        wfh_encoded,
        designation,
        resource_allocation,
        mental_fatigue
    ]], columns=[
        'Gender',
        'Company_Type',
        'WFH_Setup_Available',
        'Designation',
        'Resource_Allocation',
        'Mental_Fatigue_Score'
    ])

    # Predict burnout score
    burnout_score = float(model.predict(user_data)[0])

    # Dynamic factor impacts based on user inputs
    impact_scores = {
        "Mental Fatigue Score": mental_fatigue * 6,
        "Resource Allocation": resource_allocation * 2,
        "Designation": designation * 1.5,
        "WFH Setup Available": 5 if wfh_setup == "No" else 2,
        "Gender": 3 if gender == "Male" else 2,
        "Company Type": 3 if company_type == "Service" else 2
    }

    # Convert to percentages
    total = sum(impact_scores.values())

    feature_importance = {
        key: round((value / total) * 100, 2)
        for key, value in impact_scores.items()
    }

    # Burnout level
    if burnout_score < 0.30:
        level = "Low Burnout"
        recommendation = "Maintain current work-life balance and employee engagement."

    elif burnout_score < 0.60:
        level = "Medium Burnout"
        recommendation = "Monitor workload, encourage breaks, and improve work-life balance."

    else:
        level = "High Burnout"
        recommendation = "Reduce workload, provide wellness support, and encourage time off."

    return {
        "score": round(burnout_score, 2),
        "level": level,
        "recommendation": recommendation,
        "feature_importance": feature_importance
    }