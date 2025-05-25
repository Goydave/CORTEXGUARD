import pandas as pd
import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["has_ip"] = 1 if re.match(r"https?://\d+\.\d+\.\d+\.\d+", url) else 0
    features["suspicious_words"] = 1 if any(word in url.lower() for word in ["secure", "login", "verify", "account", "update"]) else 0
    features["https"] = 1 if urlparse(url).scheme == "https" else 0
    df = pd.DataFrame([features])
    df = df[["url_length", "num_dots", "has_ip", "suspicious_words", "https"]]
    return df