from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model

model = joblib.load('fraud_model.pkl')

# Home page

@app.route('/')
def home():
    return render_template('index.html')

# Prediction route

@app.route('/predict', methods=['POST'])
def predict():

    amount = float(request.form['amount'])
    night = int(request.form['night'])
    distance = float(request.form['distance'])
    unknown_device = int(request.form['unknown_device'])
    new_merchant = int(request.form['new_merchant'])
    foreign = int(request.form['foreign'])

    # Create dataframe

    features = pd.DataFrame([[
        amount,
        night,
        distance,
        unknown_device,
        new_merchant,
        foreign
    ]], columns=[
        'Amount',
        'Is_Night',
        'Distance_From_Home',
        'Unknown_Device',
        'New_Merchant',
        'Foreign_Transaction'
    ])

    # Predict

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1] * 100

    # Explainable AI reasons

    reasons = []

    if amount > 10000:
        reasons.append(
            "Transaction amount is unusually high"
        )

    if night == 1:
        reasons.append(
            "Transaction occurred during unusual hours"
        )

    if unknown_device == 1:
        reasons.append(
            "Login detected from unknown device"
        )

    if foreign == 1:
        reasons.append(
            "Foreign transaction detected"
        )

    if distance > 100:
        reasons.append(
            "Transaction location is far from home"
        )

    # Response

    result = {
        'fraud': bool(prediction),
        'probability': round(probability, 2),
        'reasons': reasons
    }

    return jsonify(result)

# Run server

if __name__ == '__main__':
    app.run(debug=True)