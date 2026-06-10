Here is your rewritten `README.md` that accurately matches the new project (Random Forest Regressor, multi-screen UI, bulk CSV prediction, model insight page, etc.):

```markdown
# 🧠 Employee Burnout Prediction using Machine Learning

An Artificial Intelligence and Machine Learning project that predicts employee burnout levels (a continuous value between 0 and 1) using workplace and behavioral factors. The system uses a supervised learning approach with a Random Forest Regression algorithm to analyze employee data and assess burnout risk as Low, Medium, or High.

The project combines Data Generation, Feature Engineering, Machine Learning Model Training, Feature Importance Analysis, and Flask Deployment to deliver real-time burnout predictions through a multi-screen interactive web application.

---

## 🚀 Project Highlights

* Machine Learning-Based Burnout Prediction (0.0 → 1.0 scale)
* Random Forest Regression Model
* Multi-Screen Web Application (Dashboard, Single Prediction, Bulk CSV, Model Insight)
* Animated Speedometer (Gauge) Result Visualization
* Feature Impact Analysis (% influence of each factor)
* Bulk Prediction via CSV Upload with Downloadable Results
* Dataset Schema Viewer with Data Types
* Model Performance Metrics (R², MAE, RMSE)
* End-to-End ML Deployment with Flask

---

## 📊 Problem Statement

Employee burnout is a growing challenge in modern workplaces, leading to reduced productivity, lower employee satisfaction, and increased turnover rates.

This project aims to identify employees who may be at risk of burnout by analyzing workplace-related attributes and predicting a continuous burnout score using Machine Learning techniques — for a single employee via a form, or for an entire workforce via CSV upload.

---

## 🎯 Objectives

* Predict employee burnout score (0 to 1) using Machine Learning
* Quantify how much (%) each factor impacts the prediction
* Classify employees into Low / Medium / High risk categories
* Support bulk prediction for entire teams via CSV files
* Support HR teams in proactive employee wellness management
* Demonstrate an end-to-end Machine Learning deployment pipeline

---

## 📂 Project Structure

```text
Employee-Burnout/
│
├── train_model.py              # Dataset generation + model training + evaluation
├── app.py                      # Flask application (routes & prediction logic)
├── sample_test.csv             # Sample CSV for testing bulk prediction
│
├── employee_burnout_data.csv   # Generated training dataset
├── burnout_model.pkl           # Trained Random Forest model
├── feature_impact.pkl          # Feature importance percentages
├── model_metrics.pkl           # Model evaluation metrics (R², MAE, RMSE)
│
├── templates/
│   ├── base.html               # Shared layout with navigation
│   ├── index.html              # Screen 1: Dashboard & Dataset Schema
│   ├── single.html             # Screen 2: Single Prediction + Speedometer
│   ├── bulk.html               # Screen 3: Bulk CSV Upload + Results Table
│   └── insight.html            # Screen 4: Model Insight & Metrics
│
└── static/
    ├── style.css               # Responsive dashboard design
    └── script.js               # Speedometer (Canvas) & Chart.js logic
```

---

## 📁 Project Components

### train_model.py

Responsible for:

* Dataset Generation (1,500 employee records)
* Categorical Feature Encoding
* Random Forest Model Training
* Model Evaluation (Train/Test Split — 80/20)
* Feature Importance Extraction
* Saving Model Artifacts (`.pkl` files)

### app.py

Flask application responsible for:

* Multi-Page Routing (Dashboard, Single, Bulk, Insight)
* Single Record Prediction from HTML Form
* Bulk Prediction from Uploaded CSV Files
* Input Validation & Error Handling
* Results Download (CSV Export)
* Dataset Schema Generation (columns, data types, roles)

### Frontend

#### HTML (Jinja2 Templates)

Multi-screen interface with shared navigation layout

#### CSS

Modern responsive dashboard design with cards, stat grids, risk pills, and gradient headers

#### JavaScript

* Custom Canvas-drawn animated speedometer (0 on left → 1 on right)
* Chart.js horizontal bar chart for feature impact
* Chart.js doughnut chart for bulk risk distribution

---

## 🤖 Machine Learning Workflow

### 1. Data Collection

The model is trained on an Employee Burnout dataset containing 1,500 records of employee demographic and workplace-related information.

### 2. Data Preprocessing

* Categorical Encoding (Gender, Company Type, WFH Setup)
* Feature Selection
* Data Transformation
* Target Value Clipping (0 – 1 range)

### 3. Feature Engineering

The following features are used for prediction:

| Feature              | Type        | Description                |
| -------------------- | ----------- | -------------------------- |
| Gender               | Categorical | Male / Female              |
| Company Type         | Categorical | Product / Service          |
| WFH Setup Available  | Categorical | Yes / No                   |
| Designation          | Numeric     | Employee Level (1 – 5)     |
| Resource Allocation  | Numeric     | Workload Allocation (1–10) |
| Mental Fatigue Score | Numeric     | Employee Fatigue (0–10)    |

---

## 🎯 Target Variable

The model predicts a continuous **Burn Rate** between 0 and 1, which is then mapped to risk categories:

| Burn Rate   | Burnout Level |
| ----------- | ------------- |
| 0.00 – 0.30 | 🟢 Low        |
| 0.31 – 0.60 | 🟠 Medium     |
| 0.61 – 1.00 | 🔴 High       |

This is a supervised **regression** task, with category mapping applied after prediction.

---

## 🧮 Machine Learning Algorithm

### Random Forest Regressor

The project uses a Random Forest Regression Algorithm (200 trees) from Scikit-Learn.

#### Why Random Forest?

* High Prediction Accuracy (Ensemble of Decision Trees)
* Built-in Feature Importance (used for Impact % Analysis)
* Resistant to Overfitting
* Handles Mixed Data Types
* No Feature Scaling Required (tree-based model)
* Suitable for Continuous Target Prediction (Regression)

---

## 📈 Model Evaluation

The model is evaluated on a 20% hold-out test set using:

| Metric   | Description                          |
| -------- | ------------------------------------ |
| R² Score | Variance explained by the model      |
| MAE      | Mean Absolute Error                  |
| RMSE     | Root Mean Squared Error              |

All metrics are displayed live on the **Model Insight** screen of the application.

---

## 🖥️ Application Screens

### 1️⃣ Dashboard
Dataset statistics, dataset schema (columns + data types), and feature impact (%) visualization.

### 2️⃣ Single Prediction
Employee detail form → animated speedometer gauge (0 left → 1 right) → risk category with recommendation message.

### 3️⃣ Bulk CSV Prediction
Upload a CSV of multiple employees → summary cards (Low/Medium/High counts) → risk distribution chart → top 5 highest-risk employees → full results table → downloadable results CSV.

### 4️⃣ Model Insight
Algorithm details, train/test split, evaluation metrics, and feature importance breakdown.

---

## 🖥️ Application Workflow

1. User enters employee details (or uploads a CSV file).
2. Data is sent to the Flask backend.
3. Categorical features are encoded.
4. Random Forest model generates the burnout score (0 – 1).
5. Risk category (Low / Medium / High) is determined.
6. Animated speedometer displays the result.
7. Recommendation message and factor impact (%) are shown.
8. Bulk results can be downloaded as a CSV file.

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-Learn
* Random Forest Regressor

### Data Analysis

* Pandas
* NumPy

### Data Visualization

* Chart.js (Bar & Doughnut Charts)
* HTML5 Canvas (Custom Speedometer)

### Web Development

* Flask (Jinja2 Templating)
* HTML5
* CSS3
* JavaScript

### Model Persistence

* Joblib

---

## 📚 Machine Learning Concepts Demonstrated

* Supervised Learning
* Regression
* Ensemble Learning (Random Forest)
* Feature Engineering & Encoding
* Feature Importance Analysis
* Train/Test Split & Model Evaluation
* Model Persistence & Deployment
* AI-Based Prediction Systems

---

## 💼 Real-World Applications

* Human Resource Analytics
* Employee Wellness Monitoring
* Workforce Risk Assessment
* Employee Retention Programs
* Organizational Performance Analysis
* AI-Powered Decision Support Systems

---

## ▶️ Installation & Setup

### Clone Repository

```bash
git clone https://github.com/yourusername/Employee-Burnout.git
cd Employee-Burnout
```

### Install Dependencies

```bash
pip install flask pandas scikit-learn joblib
```

### Train the Model (Run First)

```bash
python train_model.py
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

### Test Bulk Prediction

Upload the included `sample_test.csv` on the **Bulk CSV** screen, or download the sample template from the app.

---

## 📸 Project Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Single Prediction with Speedometer
![Single Prediction](screenshots/single_prediction.png)

### Bulk CSV Prediction
![Bulk Prediction](screenshots/bulk_prediction.png)

### Model Insight
![Model Insight](screenshots/model_insight.png)

---

## 🎓 Learning Outcomes

Through this project, I gained hands-on experience in:

* Machine Learning Model Development
* Random Forest Regression
* Feature Importance Analysis
* Data Preprocessing & Encoding
* Model Evaluation (R², MAE, RMSE)
* Flask Multi-Page Web Development
* CSV File Processing with Pandas
* Custom Data Visualization (Canvas Speedometer)
* Building End-to-End AI Applications

---

## 👨‍💻 Author

**Krishnam Mavani**

* GitHub: https://github.com/kano8689
* Live Link: https://employee-burnout-two.vercel.app/

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It helps support future AI, Machine Learning, and Data Analytics projects.
```

### 🔑 Key changes I made (so you can explain to faculty):

| Old README | New README | Why |
|---|---|---|
| Decision Tree **Classifier** | Random Forest **Regressor** | Your new model predicts a continuous 0–1 value, not just a class |
| Classification task | Regression task + category mapping | Matches what `train_model.py` actually does |
| `main.py`, `utils.py`, `project.ipynb` | `app.py`, `train_model.py` | Matches your actual file structure |
| Single screen | 4 screens documented | This was your faculty's main complaint — now it's a highlight |
| No metrics | R², MAE, RMSE section | Matches the Model Insight page |
| No bulk feature | Bulk CSV section + sample file | Documents the new capability |
| Matplotlib/Seaborn/Plotly | Chart.js + Canvas | You're not actually using those Python libraries in the deployed app |

📌 **Two small to-dos for you:**
1. Take fresh screenshots of all 4 screens and save them in a `screenshots/` folder with the names used above.
2. Create a `requirements.txt` with: `flask`, `pandas`, `scikit-learn`, `joblib` (since the README install section can also reference it).