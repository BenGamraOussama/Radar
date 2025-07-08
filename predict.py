import argparse
import pandas as pd
import joblib
import os

def preprocess(data):
    """Preprocess the input data as done during training."""
    data = data.copy()
    for col in ['D5', 'D6', 'D7']:
        data[col] = data[col].fillna(data[col].median())
    return data

def load_model_and_scaler(model_path='models/xgb_optimized.pkl', scaler_path='models/scaler.pkl'):
    """Load the trained model and scaler from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict(input_csv, model, scaler):
    """Make predictions on new data."""
    data = pd.read_csv(input_csv)
    processed = preprocess(data)
    features = processed[['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']]
    scaled = scaler.transform(features)
    predictions = model.predict(scaled)
    data['Predicted_Class'] = predictions
    return data

def main():
    parser = argparse.ArgumentParser(description="Predict classes for new CAN data using trained model.")
    parser.add_argument('input_csv', type=str, help="Path to input CSV file with new data.")
    parser.add_argument('--model', type=str, default='models/xgb_optimized.pkl', help="Path to trained model file.")
    parser.add_argument('--scaler', type=str, default='models/scaler.pkl', help="Path to scaler file.")
    parser.add_argument('--output_csv', type=str, default='predictions_output.csv', help="Path to save predictions CSV.")
    args = parser.parse_args()

    try:
        model, scaler = load_model_and_scaler(args.model, args.scaler)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        predictions_df = predict(args.input_csv, model, scaler)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return

    predictions_df.to_csv(args.output_csv, index=False)
    print(f"Predictions saved to {args.output_csv}")

if __name__ == "__main__":
    main()
