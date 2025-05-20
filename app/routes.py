from flask import Blueprint, render_template, request
import joblib
import pandas as pd
import re
from urllib.parse import urlparse

main = Blueprint("main", __name__)

# Load the trained model
model = joblib.load("models/phishing_model.pkl")

# Feature extraction
def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["has_ip"] = 1 if re.match(r"https?://\d+\.\d+\.\d+\.\d+", url) else 0
    features["suspicious_words"] = 1 if any(word in url.lower() for word in ["secure", "login", "verify", "account", "update"]) else 0
    features["https"] = 1 if urlparse(url).scheme == "https" else 0

    # 🔥 FORCE column order exactly like the model expects
    df = pd.DataFrame([features])
    df = df[["url_length", "num_dots", "has_ip", "suspicious_words", "https"]]
    return df


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url")
    features = extract_features(url)
    prediction = model.predict(features)[0]
    label = "Phishing 🚨" if prediction == 1 else "Legit ✅"
    return render_template("result.html", url=url, prediction=label)
