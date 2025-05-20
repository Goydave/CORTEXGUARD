import pandas as pd
from urllib.parse import urlparse

# Load the combined dataset
df = pd.read_csv("processed/combined_dataset.csv")

# Feature 1: URL Length
df['url_length'] = df['url'].apply(len)

# Feature 2: Number of dots in URL
df['num_dots'] = df['url'].apply(lambda x: x.count('.'))

# Feature 3: Has IP Address (True if domain is an IP)
import re
def has_ip(url):
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    return int(bool(re.search(ip_pattern, urlparse(url).netloc)))
df['has_ip'] = df['url'].apply(has_ip)

# Feature 4: Count of suspicious words
suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'webscr']
def count_suspicious_words(url):
    return sum(word in url.lower() for word in suspicious_words)
df['suspicious_words'] = df['url'].apply(count_suspicious_words)

# Feature 5: Use of HTTPS (0 or 1)
df['https'] = df['url'].apply(lambda x: int(urlparse(x).scheme == 'https'))

# Save extracted features + label only
features_df = df[['url_length', 'num_dots', 'has_ip', 'suspicious_words', 'https', 'label']]
features_df.to_csv("processed/features.csv", index=False)

print(f"✅ Feature extraction complete. Saved to processed/features.csv with {len(features_df)} rows.")
