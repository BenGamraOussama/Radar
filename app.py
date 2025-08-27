from flask import Flask, request, jsonify, render_template, send_from_directory
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

# Load models and scalers on startup
FLAG_MODEL_PATH = 'models/flag_model/best_flag_model.pkl'
FLAG_SCALER_PATH = 'models/Random_forest/scaler.pkl'
SOURCE_MODEL_PATH = 'models/flag_model/best_source_model.pkl'
SOURCE_SCALER_PATH = 'models/Random_forest/scaler.pkl'

# Check if files exist
for path in [FLAG_MODEL_PATH, FLAG_SCALER_PATH, SOURCE_MODEL_PATH, SOURCE_SCALER_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model or scaler file not found: {path}")

# Load all models and scalers
flag_model = joblib.load(FLAG_MODEL_PATH)
flag_scaler = joblib.load(FLAG_SCALER_PATH)
source_model = joblib.load(SOURCE_MODEL_PATH)
source_scaler = joblib.load(SOURCE_SCALER_PATH)

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data for both models"""
    for col in ['D5', 'D6', 'D7']:
        if col in data.columns:
            data[col] = data[col].fillna(data[col].median())
    return data

def make_predictions(input_data: PredictionInput):
    """Make predictions with both models"""
    # Convert input list to DataFrame
    if len(input_data.data) != 8:
        raise ValueError("Input data must contain exactly 8 features corresponding to D0 to D7.")
    
    df = pd.DataFrame([input_data.data], columns=['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'])
    processed = preprocess(df)
    features = processed[['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']]
    
    # Flag prediction
    flag_scaled = flag_scaler.transform(features)
    flag_prediction = flag_model.predict(flag_scaled)
    flag_probs = flag_model.predict_proba(flag_scaled).tolist()[0] if hasattr(flag_model, "predict_proba") else []
    
    # Source prediction
    source_scaled = source_scaler.transform(features)
    source_prediction = source_model.predict(source_scaled)
    source_probs = source_model.predict_proba(source_scaled).tolist()[0] if hasattr(source_model, "predict_proba") else []
    
    return {
        "flag": {
            "predicted_class": int(flag_prediction[0]),
            "probabilities": flag_probs,
            "class_labels": ["R", "T"]
        },
        "source": {
            "predicted_class": int(source_prediction[0]),
            "probabilities": source_probs,
            "class_labels": [f"Source {i}" for i in range(len(source_probs))]
        },
        "input_data": input_data.data
    }

@app.route('/')
def home():
    return send_from_directory('.', 'client.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = PredictionInput.model_validate(request.get_json())
        pred = make_predictions(data)
        return jsonify({
            "predictions": pred,
            "status": "success"
        })
    except ValidationError as e:
        return jsonify({"error": str(e), "status": "error"}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve), "status": "error"}), 400
    except Exception as ex:
        return jsonify({"error": "Prediction error: " + str(ex), "status": "error"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)