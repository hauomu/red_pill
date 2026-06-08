import pandas as pd
import sqlite3

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
print("SAMPLE COMMENTS")
print("=" * 100)
print("\nPositive (5-star) samples:")
positive = df[df['rating'] == 5.0]['comment'].head(5)
for i, comment in enumerate(positive, 1):
    print(f"{i}. {comment[:80]}...")

print("\nNegative (1-2 star) samples:")
negative = df[df['rating'] <= 2.0]['comment'].head(5)
for i, comment in enumerate(negative, 1):
    print(f"{i}. {comment[:80]}...")

# Define themes and keywords
themes = {
    'Delivery Speed': ['fast', 'slow', 'quick', 'delay', 'late', 'speed', 'on time', 'early', 'urgent', 'wait', 'took long', 'scheduled', 'window', 'promise'],
    'Service Quality': ['service', 'professional', 'polite', 'rude', 'friendly', 'helpful', 'attitude', 'courteous', 'behavior', 'unprofessional', 'responsive'],
    'Packaging/Condition': ['package', 'damage', 'broken', 'intact', 'box', 'wrapping', 'careful', 'careless', 'condition', 'packed', 'damaged', 'dent', 'crushed'],
    'Communication': ['communication', 'update', 'notification', 'informed', 'contacted', 'message', 'call', 'response', 'call ahead', 'informed'],
    'Tracking': ['location', 'track', 'gps', 'address', 'wrong', 'lost', 'route', 'where'],
    'Driver Performance': ['driver', 'rider', 'delivery person', 'staff', 'excellent', 'poor', 'behavior'],
    'Cost/Pricing': ['price', 'cost', 'expensive', 'cheap', 'value', 'fee', 'charge', 'affordable'],
    'Reliability': ['reliable', 'consistent', 'dependable', 'always', 'every time', 'repeated', 'trust'],
    'Cleanliness': ['clean', 'dirty', 'neat', 'organized', 'hygiene', 'mess'],
    'Safety': ['safe', 'security', 'protect', 'careful', 'fragile']
}

# Categorize comments
def categorize_comment(comment):
    comment_lower = str(comment).lower() if comment else ""
    for theme, keywords in themes.items():
        for keyword in keywords:
            if keyword.lower() in comment_lower:
                return theme
    return 'Other'

df['theme'] = df['comment'].apply(categorize_comment)

# Count by theme
print("\n" + "=" * 100)
print("THEME DISTRIBUTION")
print("=" * 100)
theme_counts = df['theme'].value_counts()
theme_pcts = (df['theme'].value_counts(normalize=True) * 100).round(1)

for theme in sorted(df['theme'].unique()):
    count = theme_counts[theme]
    pct = theme_pcts[theme]
    print(f"  {theme:25s}: {pct:6.1f}% ({count:,} comments)")

# Show top comments per theme
print("\n" + "=" * 100)
print("TOP POSITIVE & NEGATIVE COMMENTS BY THEME")
print("=" * 100)

theme_summary = {}

for theme in sorted(df['theme'].unique()):
    theme_df = df[df['theme'] == theme]
    
    positive = theme_df[theme_df['rating'] >= 4]['comment'].head(5).tolist()
    negative = theme_df[theme_df['rating'] <= 2]['comment'].head(5).tolist()
    
    # Store for later use
    theme_summary[theme] = {
        'count': len(theme_df),
        'pct': (len(theme_df) / len(df) * 100),
        'positive': positive,
        'negative': negative
    }
    
    print(f"\n{theme} ({len(theme_df)} comments, {len(theme_df)/len(df)*100:.1f}%)")
    print("-" * 100)
    
    if positive:
        print("  TOP 5 Positive (4-5 stars):")
        for i, comment in enumerate(positive, 1):
            print(f"    {i}. {comment[:85]}...")
    else:
        print("  TOP 5 Positive (4-5 stars): None found")
    
    if negative:
        print("  TOP 5 Negative (1-2 stars):")
        for i, comment in enumerate(negative, 1):
            print(f"    {i}. {comment[:85]}...")
    else:
        print("  TOP 5 Negative (1-2 stars): None found")

print("\n" + "=" * 100)
print("✅ ANALYSIS COMPLETE - Ready to add to Excel")
print("=" * 100)
