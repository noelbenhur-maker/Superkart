import os
import joblib
import pandas as pd
import io
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the serialized model pipeline
model_path = os.path.join(os.path.dirname(__file__), "superkart_model.joblib")
model = joblib.load(model_path)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/v1/predict", methods=["POST"])
def predict():
    try:
        # Get JSON payload
        data = request.get_json(force=True)
        
        # Convert payload to DataFrame (single row)
        df_input = pd.DataFrame([data])
        
        # Predict
        prediction = model.predict(df_input)[0]
        return jsonify({"prediction": float(prediction)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    try:
        # Check if file is part of request
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
            
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
            
        # Read CSV file contents
        file_bytes = file.read()
        df_input = pd.read_csv(io.BytesIO(file_bytes))
        
        # Predict for all rows
        predictions = model.predict(df_input)
        
        # Map index to predictions
        output = {str(idx): float(pred) for idx, pred in enumerate(predictions)}
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Run on port 7860 to match expected ports
    app.run(host="0.0.0.0", port=7860)
