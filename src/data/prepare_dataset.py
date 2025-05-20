import pandas as pd

# Load phishing URLs
with open("raw/phishing.txt", "r") as f:
    phishing_urls = [line.strip() for line in f if line.strip()]  # remove empty lines
phishing_df = pd.DataFrame(phishing_urls, columns=["url"])
phishing_df["label"] = 1

print(f"✅ Loaded {len(phishing_df)} phishing URLs.")

# Load legit URLs
legit_df = pd.read_csv("raw/final_legit.csv", header=None, names=["url"])
legit_df["label"] = 0

print(f"✅ Loaded {len(legit_df)} legit URLs.")

# Combine both
combined_df = pd.concat([phishing_df, legit_df], ignore_index=True)

# Shuffle the dataset
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the processed dataset
combined_df.to_csv("processed/combined_dataset.csv", index=False)

print(f"✅ Combined dataset created with {len(combined_df)} rows.")
print(combined_df['label'].value_counts())

