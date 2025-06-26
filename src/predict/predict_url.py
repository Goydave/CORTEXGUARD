import sys
import joblib
import pandas as pd
import math
from urllib.parse import urlparse
import re

# 🚨 URL from command line
url = sys.argv[1]
print(f"🔍 URL: {url}")

# Suspicious words and shorteners
SUSPICIOUS_WORDS = ['login', 'verify', 'update', 'secure', 'account', 'webscr', 'bank', 'signin']
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly"]

# ✅ Helper: calculate entropy
def calculate_entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(string)]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob]) if len(string) > 0 else 0

# ✅ Feature extraction
def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path + parsed.query

    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "has_ip": int(bool(re.match(r"(\d{1,3}\.){3}\d{1,3}", domain))),
        "https": int(parsed.scheme == "https"),
        "suspicious_words": sum(word in url.lower() for word in SUSPICIOUS_WORDS),
        "num_special_chars": sum(url.count(c) for c in ['@', '%', '=', '-', '_', '!', '?', '&']),
        "is_shortened": int(any(short in domain for short in SHORTENERS)),
        "domain_entropy": calculate_entropy(domain)
    }

# ✅ Load model
model = joblib.load("models/phishing_model.pkl")

# ✅ Predict
features = pd.DataFrame([extract_features(url)])
prediction = model.predict(features)[0]

# ✅ Output
print("🧠 Prediction:", "Phishing 🚨" if prediction == 1 else "Legit ✅")
