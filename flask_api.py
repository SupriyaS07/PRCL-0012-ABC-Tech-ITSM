from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from database import get_summary_stats, get_monthly_volume
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# ── Load all models ────────────────────────────────
try:
    model_uc1       = joblib.load('models/model_uc1.pkl')
    model_uc3       = joblib.load('models/model_uc3.pkl')
    uc1_features    = joblib.load('models/uc1_features.pkl')
    uc3_features    = joblib.load('models/uc3_features.pkl')
    label_mapping   = joblib.load('models/label_mapping.pkl')
    reverse_mapping = joblib.load('models/reverse_mapping.pkl')
    print("✅ All models loaded!")
except Exception as e:
    print(f"❌ Model loading error: {e}")


# ── Home ───────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({'message': 'PRCL-0012 ITSM API is running!'})


# ── Summary Stats ──────────────────────────────────
@app.route('/api/summary', methods=['GET'])
def summary():
    try:
        stats = get_summary_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error'   : str(e),
            'total'   : 0,
            'priority': [],
            'category': [],
            'yearly'  : []
        }), 200


# ── UC1 — High Priority Prediction ────────────────
@app.route('/api/predict_priority', methods=['POST'])
def predict_priority():
    try:
        data     = request.json
        input_df = pd.DataFrame([data], columns=uc1_features)
        input_df = input_df.astype(float)

        prediction  = model_uc1.predict(input_df)[0]
        probability = model_uc1.predict_proba(input_df)[0]

        return jsonify({
            'prediction': int(prediction),
            'label'     : 'High Priority' if prediction == 1 else 'Normal Priority',
            'confidence': round(float(max(probability)) * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── UC2 — Incident Volume Forecast ────────────────
@app.route('/api/forecast', methods=['POST'])
def forecast():
    try:
        data    = request.json
        periods = int(data.get('periods', 6))

        # Try to fetch from MySQL
        monthly = get_monthly_volume()

        # If MySQL fails use hardcoded historical data
        if monthly.empty:
            print("⚠️ MySQL unavailable — using cached historical data")
            monthly = pd.DataFrame({
                'year' : [2013]*11 + [2014]*12,
                'month': [1,2,3,4,5,7,8,9,10,11,12,
                          1,2,3,4,5,6,7,8,9,10,11,12],
                'count': [1086,1128,1061,1460,959,967,791,871,873,1186,910,
                          19,468,1412,954,873,1389,1193,416,391,1230,845,713]
            })

        # Replace outliers
        median_val = monthly['count'].median()
        monthly.loc[
            (monthly['year'] == 2013) & (monthly['month'] == 6), 'count'
        ] = median_val

        # Fit ARIMA
        arima_model   = ARIMA(monthly['count'].values, order=(2, 1, 2))
        arima_fit     = arima_model.fit()
        forecast_vals = arima_fit.forecast(steps=periods)

        return jsonify({
            'forecast': [round(float(f), 0) for f in forecast_vals],
            'periods' : periods
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── UC3 — Auto Tag Priority ────────────────────────
@app.route('/api/auto_tag', methods=['POST'])
def auto_tag():
    try:
        data     = request.json
        input_df = pd.DataFrame([data], columns=uc3_features)
        input_df = input_df.astype(float)

        prediction  = model_uc3.predict(input_df)[0]
        probability = model_uc3.predict_proba(input_df)[0]

        return jsonify({
            'predicted_priority': int(prediction),
            'label'             : f'Priority {int(prediction)}',
            'confidence'        : round(float(max(probability)) * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Run ────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
