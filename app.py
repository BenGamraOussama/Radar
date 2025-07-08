from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel, Field, ValidationError
from typing import List, Annotated
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

class PredictionInput(BaseModel):
    data: Annotated[List[float], Field(min_length=1)]

# Load model and scaler on startup
MODEL_PATH = 'models/xgb_optimized.pkl'
SCALER_PATH = 'models/scaler.pkl'

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Model or scaler file not found. Please ensure they exist in the 'models/' directory.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    for col in ['D5', 'D6', 'D7']:
        if col in data.columns:
            data[col] = data[col].fillna(data[col].median())
    return data

def make_prediction(input_data: PredictionInput):
    # Convert input list to DataFrame with expected columns
    # Assuming input_data.data is a list of floats corresponding to features D0 to D7
    if len(input_data.data) != 8:
        raise ValueError("Input data must contain exactly 8 features corresponding to D0 to D7.")
    df = pd.DataFrame([input_data.data], columns=['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'])
    processed = preprocess(df)
    features = processed[['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']]
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)
    # If model supports predict_proba, get probabilities
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(scaled).tolist()[0]
    else:
        probabilities = []
    return {
        "predicted_class": int(prediction[0]),
        "probabilities": probabilities,
        "input_data": input_data.data
    }

from flask import send_from_directory

@app.route('/')
def home():
    return send_from_directory('.', 'client.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = PredictionInput.model_validate(request.get_json())
        pred = make_prediction(data)
        return jsonify({
            "prediction": pred,
            "status": "success"
        })
    except ValidationError as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400
    except ValueError as ve:
        return jsonify({
            "error": str(ve),
            "status": "error"
        }), 400
    except Exception as ex:
        return jsonify({
            "error": "Prediction error: " + str(ex),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
