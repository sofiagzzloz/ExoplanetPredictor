from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from joblib import load

app = Flask(__name__)
CORS(app)
model = load('/Users/sofiagonzalez/Desktop/Innovation Engineering/my_trained_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    probabilities = model.predict_proba([data['features']])
    # 1 = positive(exoplanet) 0 = false
    probability_of_exoplanet = probabilities[0][1]
    prediction = 1 if probability_of_exoplanet > 0.5 else 0
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True)