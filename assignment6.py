import pandas as pd
import numpy as np
import re
from collections import Counter

# --- Step 1: Load and Merge Datasets ---
speeches = pd.read_csv("speeches.csv", usecols=["date", "contents"])
fx = pd.read_csv("fx.csv")

# Standardize column names (assuming fx has date and a rate column)
fx.columns = [col.lower() for col in fx.columns]
# Rename the actual price column to 'rate' if it's named 'obs_value' or similar
if 'obs_value' in fx.columns:
    fx = fx.rename(columns={'obs_value': 'rate'})

# Convert dates to datetime objects for accurate handling
speeches['date'] = pd.to_datetime(speeches['date'])
fx['date'] = pd.to_datetime(fx['date'])

# Merge keeping all fx rows (left join if fx is left, or right join)
df = pd.merge(fx, speeches, on='date', how='left')

# --- Step 2: Remove obvious outliers or mistakes ---
# Ensure exchange rates are numeric, turn invalid strings into NaN
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
# Remove extreme outliers (e.g., negative rates or values completely out of normal bounds)
df = df[df['rate'] > 0]

# --- Step 3: Handle missing observations ---
df = df.sort_values('date').reset_index(drop=True)
# Replace missing exchange rates with the latest available (Forward Fill)
df['rate'] = df['rate'].ffill()
# Remove entries where no historical information is available to fill forward
df = df.dropna(subset=['rate'])

# --- Step 4: Calculate Return and Indicators ---
# Exchange rate return: (Pt - Pt-1) / Pt-1
df['return'] = df['rate'].pct_change()

df['good_news'] = np.where(df['return'] > 0.005, 1, 0)
df['bad_news'] = np.where(df['return'] < -0.005, 1, 0)

# --- Step 5: Text Processing & Top 20 Words ---
# Drop entries where contents column has NA values
df_text = df.dropna(subset=['contents']).copy()

# Basic Stopwords list to filter out articles, prepositions, etc.
STOPWORDS = set([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", 
    "by", "of", "from", "is", "are", "was", "were", "be", "been", "this", "that", 
    "it", "as", "by", "not", "by", "we", "our", "will", "have", "has", "can", "it's"
])

def get_top_words(text_series, n=20):
    all_words = []
    for text in text_series:
        # Lowercase and clean words using regex
        words = re.findall(r'\b[a-z]{3,}\b', str(text).lower())
        filtered_words = [w for w in words if w not in STOPWORDS]
        all_words.extend(filtered_words)
    
    return pd.DataFrame(Counter(all_words).most_common(n), columns=['word', 'count'])

# Generate tables
good_indicators = get_top_words(df_text[df_text['good_news'] == 1]['contents'])
bad_indicators = get_top_words(df_text[df_text['bad_news'] == 1]['contents'])

# Save to CSV
good_indicators.to_csv("good_indicators.csv", index=False)
bad_indicators.to_csv("bad_indicators.csv", index=False)

print("Python execution complete. CSV files generated.")
