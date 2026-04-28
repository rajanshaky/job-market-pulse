import pandas as pd

df = pd.read_csv('data/processed/job_listings_clean.csv')

print("=== TOP 10 HIRING CITIES ===")
print(df['city'].value_counts().head(10))

print("\n=== JOBS BY CATEGORY ===")
print(df['category'].value_counts())

print("\n=== TOP 10 HIRING COMPANIES ===")
print(df['company'].value_counts().head(10))

print("\n=== JOBS BY SEARCH KEYWORD ===")
print(df['search_keyword'].value_counts())

print("\n=== JOBS BY MONTH ===")
print(df['month'].value_counts().sort_index())
