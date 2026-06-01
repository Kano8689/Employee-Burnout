from flask import Flask, render_template, jsonify
from utils import train_burnout_model, calculate_form_burnout

app = Flask(__name__)

# Train model when application starts
try:
    train_burnout_model()
except Exception as e:
    raise Exception(f"Model training failed: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        result = calculate_form_burnout()

        return jsonify({
            "success": True,
            "score": result["score"],
            "level": result["level"],
            "recommendation": result["recommendation"],
            "importance": result["feature_importance"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True)