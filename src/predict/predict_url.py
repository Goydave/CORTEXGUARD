import pandas as pd
import re
from urllib.parse import urlparse
import joblib
import sys

# Load the trained model
with open("models/phishing_model.pkl", "rb") as f:
    model = joblib.load(f)

# Feature extraction function
def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["has_ip"] = 1 if re.match(r"https?://\d+\.\d+\.\d+\.\d+", url) else 0
    features["suspicious_words"] = 1 if any(word in url.lower() for word in ["secure", "login", "verify", "account", "update"]) else 0
    features["https"] = 1 if urlparse(url).scheme == "https" else 0
    return pd.DataFrame([features])

# Get URL from command line
if len(sys.argv) != 2:
    print("⚠️ Usage: python src/predict/predict_url.py <url>")
    sys.exit(1)

url = sys.argv[1]
features = extract_features(url)
prediction = model.predict(features)[0]

label = "Phishing 🚨" if prediction == 1 else "Legit ✅"
print(f"🔍 URL: {url}\n🧠 Prediction: {label}")
