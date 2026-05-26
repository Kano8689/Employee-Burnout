from flask import Flask, render_template, jsonify
from utils import train_burnout_model, calculate_form_burnout

app = Flask(__name__)

# Pre-train the decision tree when the server initializes
try:
    train_burnout_model()
except Exception as e:
    print(f"Error training model on initialization: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Let utils.py extract the form fields and compute the results
        prediction_score = calculate_form_burnout()
        
        # Dispatch the scalar float value to your front-end JS listener
        return jsonify({'success': True, 'prediction': prediction_score})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)