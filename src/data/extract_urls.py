import pandas as pd

# Load the csv.txt file (ensure it's comma-separated)
df = pd.read_csv("csv.txt")

# Check if 'url' column exists
if 'url' not in df.columns:
    raise ValueError("❌ The column 'url' was not found in the file. Please check the header.")

# Extract the 'url' column, drop NaNs and duplicates
url_df = df[['url']].dropna().drop_duplicates()

# Save to clean_csv.txt (no header, no index)
url_df.to_csv("clean_csv.txt", index=False, header=False)

print(f"✅ Extracted and saved {len(url_df)} unique URLs to data/clean_csv.txt")
