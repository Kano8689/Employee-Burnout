from flask import Flask, render_template, request, redirect, url_for, send_file
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load Model and Feature Impacts
model = joblib.load('burnout_model.pkl')
feature_impact = joblib.load('feature_impact.pkl')
FEATURES = ['Work_Hours', 'Mental_Fatigue_Score', 'Resource_Allocation', 'WFH_Setup_Available', 'Designation']

@app.route('/')
def home():
    return render_template('index.html', impact=feature_impact)

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/predict_single', methods=['POST'])
def predict_single():
    try:
        # Get form data
        input_data = [[
            float(request.form['Work_Hours']),
            float(request.form['Mental_Fatigue_Score']),
            float(request.form['Resource_Allocation']),
            float(request.form['WFH_Setup_Available']),
            float(request.form['Designation'])
        ]]
        
        # Predict
        prediction = model.predict(input_data)[0]
        prediction = max(0.0, min(1.0, prediction)) # Ensure between 0 and 1
        
        return render_template('single.html', prediction=round(prediction, 3), impact=feature_impact)
    except Exception as e:
        return str(e)

@app.route('/bulk')
def bulk():
    return render_template('bulk.html')

@app.route('/predict_bulk', methods=['POST'])
def predict_bulk():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
        
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        
        # Ensure columns match
        for col in FEATURES:
            if col not in df.columns:
                return f"Error: CSV missing column '{col}'"
                
        # Predict
        X = df[FEATURES]
        df['Predicted_Burnout'] = model.predict(X).clip(0, 1).round(3)
        
        # Save to show on screen and allow download
        results_path = 'static/predicted_results.csv'
        df.to_csv(results_path, index=False)
        
        # Convert to HTML table for the "multi-screen" UI requirement
        table_html = df.to_html(classes='table table-striped', index=False)
        
        return render_template('bulk.html', table=table_html, show_download=True)

@app.route('/download')
def download():
    return send_file('static/predicted_results.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)