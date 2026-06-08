import pandas as pd
import sqlite3
import re
from collections import Counter

print("📊 Analyzing feedback comments to identify themes...")

# Load feedback comments from database
conn = sqlite3.connect('delivery.db')
query = """
SELECT 
    feedback_id,
    rating,
    comment
FROM feedback
WHERE comment IS NOT NULL AND TRIM(comment) != ''
ORDER BY feedback_id
"""

df = pd.read_sql_query(query, conn)
conn.close()

print(f"Total feedback records with comments: {len(df)}\n")

# Show sample comments
print("=" * 100)
print("SAMPLE COMMENTS (First 20)")
print("=" * 100)
print("\nPositive (5-star) samples:")
positive = df[df['rating'] == 5.0]['comment'].head(5)
for i, comment in enumerate(positive, 1):
    print(f"{i}. {comment[:80]}...")

print("\nNegative (1-2 star) samples:")
negative = df[df['rating'] <= 2.0]['comment'].head(5)
for i, comment in enumerate(negative, 1):
    print(f"{i}. {comment[:80]}...")

print("\nNeutral/Mixed (3-4 star) samples:")
neutral = df[(df['rating'] == 3.0) | (df['rating'] == 4.0)]['comment'].head(5)
for i, comment in enumerate(neutral, 1):
    print(f"{i}. {comment[:80]}...")

# Keyword-based theme categorization
print("\n" + "=" * 100)
print("ANALYZING THEMES BY KEYWORDS")
print("=" * 100)

# Define themes and keywords
themes = {
    'Delivery Speed': ['fast', 'slow', 'quick', 'delay', 'late', 'speed', 'on time', 'early', 'urgent', 'wait', 'took long'],
    'Service Quality': ['service', 'professional', 'polite', 'rude', 'friendly', 'helpful', 'attitude', 'courteous', 'behavior', 'unprofessional'],
    'Packaging/Condition': ['package', 'damage', 'broken', 'intact', 'box', 'wrapping', 'careful', 'careless', 'condition', 'packed'],
    'Communication': ['communication', 'update', 'notification', 'informed', 'contacted', 'message', 'call', 'response', 'tracking'],
    'Tracking/Location': ['location', 'track', 'gps', 'address', 'wrong', 'lost', 'route', 'map'],
    'Driver Performance': ['driver', 'rider', 'delivery person', 'staff', 'professional'],
    'Cost/Pricing': ['price', 'cost', 'expensive', 'cheap', 'value', 'fee', 'charge'],
    'Safety': ['safe', 'security', 'safe handling', 'protect', 'careful delivery'],
    'Reliability': ['reliable', 'consistent', 'dependable', 'always', 'every time', 'repeated'],
    'Cleanliness': ['clean', 'dirty', 'neat', 'organized', 'hygiene']
}

# Categorize comments
df['theme'] = 'Other'
df['all_keywords'] = []

for idx, row in df.iterrows():
    comment_lower = str(row['comment']).lower()
    matched_themes = []
    
    for theme, keywords in themes.items():
        for keyword in keywords:
            if keyword.lower() in comment_lower:
                matched_themes.append(theme)
                break
    
    if matched_themes:
        df.at[idx, 'theme'] = matched_themes[0]  # Primary theme
        df.at[idx, 'all_keywords'] = matched_themes

# Count by theme
print("\nTheme Distribution:")
theme_counts = df['theme'].value_counts()
print(theme_counts)

print("\nTheme Percentages:")
theme_pcts = (df['theme'].value_counts() / len(df) * 100).round(1)
for theme, pct in theme_pcts.items():
    print(f"  {theme:25s}: {pct:6.1f}% ({theme_counts[theme]:,} comments)")

# Show top comments per theme
print("\n" + "=" * 100)
print("TOP 5 POSITIVE & NEGATIVE COMMENTS BY THEME")
print("=" * 100)

for theme in sorted(df['theme'].unique()):
    theme_df = df[df['theme'] == theme]
    
    if len(theme_df) == 0:
        continue
    
    positive = theme_df[theme_df['rating'] >= 4]['comment'].head(5).tolist()
    negative = theme_df[theme_df['rating'] <= 2]['comment'].head(5).tolist()
    
    print(f"\n{theme} ({len(theme_df)} comments)")
    print("-" * 100)
    
    if positive:
        print("  Positive (4-5 stars):")
        for i, comment in enumerate(positive, 1):
            print(f"    {i}. {comment[:90]}...")
    else:
        print("  Positive (4-5 stars): None")
    
    if negative:
        print("  Negative (1-2 stars):")
        for i, comment in enumerate(negative, 1):
            print(f"    {i}. {comment[:90]}...")
    else:
        print("  Negative (1-2 stars): None")

print("\n" + "=" * 100)
print("✅ ANALYSIS COMPLETE - Ready to add to Excel")
print("=" * 100)
