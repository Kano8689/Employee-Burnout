# 🧠 Employee Burnout Prediction using Machine Learning

An Artificial Intelligence and Machine Learning project that predicts employee burnout levels using workplace and behavioral factors. The system leverages a supervised learning approach with a Decision Tree Classification algorithm to analyze employee data and classify burnout risk into Low, Medium, or High categories.

The project combines Data Preprocessing, Feature Engineering, Machine Learning Model Training, and Flask Deployment to deliver real-time burnout predictions through an interactive web application.

---

## 🚀 Project Highlights

* Machine Learning-Based Burnout Prediction
* Employee Risk Assessment System
* Decision Tree Classification Model
* Interactive Burnout Gauge Dashboard
* Real-Time Prediction Interface
* End-to-End ML Deployment with Flask
* Responsive User Interface

---

## 📊 Problem Statement

Employee burnout is a growing challenge in modern workplaces, leading to reduced productivity, lower employee satisfaction, and increased turnover rates.

This project aims to identify employees who may be at risk of burnout by analyzing workplace-related attributes and predicting burnout levels using Machine Learning techniques.

---

## 🎯 Objectives

* Predict employee burnout levels using Machine Learning
* Analyze workplace and behavioral factors affecting burnout
* Classify employees into risk categories
* Support HR teams in proactive employee wellness management
* Demonstrate an end-to-end Machine Learning deployment pipeline

---

## 📂 Project Structure

```text
Employee-Burnout/
│
├── main.py
├── utils.py
├── project.ipynb
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
│
├── templates/
│   └── index.html
│
└── Datasets/
    └── employee_burnout.csv
```

---

## 📁 Project Components

### project.ipynb

Contains:

* Data Cleaning
* Data Preprocessing
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Machine Learning Model Development
* Model Evaluation

### utils.py

Responsible for:

* Dataset Loading
* Data Transformation
* Feature Encoding
* Model Training
* Prediction Logic

### main.py

Flask application responsible for:

* User Interface Integration
* Request Handling
* Real-Time Predictions
* API Routing

### Frontend

#### HTML

Interactive employee input form

#### CSS

Modern responsive dashboard design

#### JavaScript

Prediction requests and dynamic result visualization

---

## 🤖 Machine Learning Workflow

### 1. Data Collection

The model is trained using an Employee Burnout dataset containing employee demographic and workplace-related information.

### 2. Data Preprocessing

* Missing Value Removal
* Data Cleaning
* Feature Selection
* Categorical Encoding
* Data Transformation

### 3. Feature Engineering

The following features are used for prediction:

| Feature              | Description                |
| -------------------- | -------------------------- |
| Gender               | Male / Female              |
| Company Type         | Product / Service          |
| WFH Setup Available  | Yes / No                   |
| Designation          | Employee Designation Level |
| Resource Allocation  | Workload Allocation        |
| Mental Fatigue Score | Employee Fatigue Level     |

---

## 🎯 Target Variable

The original Burn Rate is transformed into burnout categories:

| Burn Rate   | Burnout Level |
| ----------- | ------------- |
| ≤ 0.30      | Low           |
| 0.31 – 0.60 | Medium        |
| > 0.60      | High          |

This converts the problem into a supervised multiclass classification task.

---

## 🧮 Machine Learning Algorithm

### Decision Tree Classifier

The project uses a Decision Tree Classification Algorithm from Scikit-Learn.

#### Why Decision Tree?

* Easy to Interpret
* Fast Training
* Fast Prediction
* Handles Mixed Data Types
* Suitable for Classification Problems
* Requires Minimal Data Preparation

---

## 🔬 Model Training Process

1. Load Employee Burnout Dataset
2. Clean Dataset
3. Remove Missing Values
4. Encode Categorical Features
5. Create Burnout Categories
6. Split Dataset into Training and Testing Sets
7. Train Decision Tree Classifier
8. Generate Predictions
9. Deploy Model with Flask

---

## 📈 Prediction Categories

The trained model predicts one of the following burnout levels:

### 🟢 Low Burnout

Burnout Score: 0.00 – 0.30

Employee is working under healthy conditions with manageable stress levels.

---

### 🟠 Medium Burnout

Burnout Score: 0.31 – 0.60

Employee may be experiencing moderate work-related stress and should be monitored.

---

### 🔴 High Burnout

Burnout Score: 0.61 – 1.00

Employee is likely experiencing significant burnout and may require intervention.

---

## 🖥️ Application Workflow

1. User enters employee details.
2. Data is sent to the Flask backend.
3. Features are encoded.
4. Decision Tree model generates prediction.
5. Burnout category is determined.
6. Interactive gauge displays the result.
7. Recommendation message is shown.

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-Learn
* Decision Tree Classifier

### Data Analysis

* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn
* Plotly

### Web Development

* Flask
* HTML5
* CSS3
* JavaScript

### Development Environment

* Jupyter Notebook

---

## 📚 Machine Learning Concepts Demonstrated

* Supervised Learning
* Classification
* Feature Engineering
* Data Preprocessing
* Decision Trees
* Model Training
* Model Deployment
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
pip install -r requirements.txt
```

### Run Application

```bash
python main.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

---

## 📸 Screenshots

Add project screenshots here:

```text
screenshots/homepage.png
screenshots/prediction-result.png
screenshots/dashboard.png
```

---

## 🎓 Learning Outcomes

Through this project, I gained hands-on experience in:

* Machine Learning Model Development
* Decision Tree Classification
* Data Cleaning and Preprocessing
* Feature Engineering
* Flask Web Development
* Model Deployment
* Frontend and Backend Integration
* Building End-to-End AI Applications

---

## 👨‍💻 Author

**Krishnam Mavani**

* GitHub: https://github.com/kano8689

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It helps support future AI, Machine Learning, and Data Analytics projects.
