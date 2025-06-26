import pandas as pd
import re
import math
from urllib.parse import urlparse

# Load dataset
df = pd.read_csv("src/data/processed/combined_dataset.csv")

# Suspicious words list
SUSPICIOUS_WORDS = ['login', 'verify', 'update', 'secure', 'account', 'webscr', 'bank', 'signin']

# Shortened domains
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly"]

# Shannon entropy function
def calculate_entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(string)]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob]) if len(string) > 0 else 0

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

# Extract features
features = df["url"].apply(lambda x: extract_features(x))
features_df = pd.DataFrame(features.tolist())
features_df["label"] = df["label"]

# Save to file
features_df.to_csv("src/data/processed/features.csv", index=False)
print(f"✅ Enhanced features saved to src/data/processed/features.csv with {len(features_df)} rows.")
