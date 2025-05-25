import os
from flask import Blueprint, render_template, request
import joblib
import pandas as pd
import re
from urllib.parse import urlparse
from src.predict.predict_url import extract_features

main = Blueprint("main", __name__)

# ─── Determine project root & model path ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))    # .../CORTEXGUARD/app
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))  # .../CORTEXGUARD
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "phishing_model.pkl")

# Load the trained model
with open("models/phishing_model.pkl", "rb") as f:
    model = joblib.load(f)

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url")
    features = extract_features(url)
    if "https" in features.columns:
        features["https"] = 0
    print("Features for prediction (forced https=0):", features)
    prediction = model.predict(features)[0]
    label = "Phishing 🚨" if prediction == 1 else "Legit ✅"
    return render_template("result.html", url=url, prediction=label)
