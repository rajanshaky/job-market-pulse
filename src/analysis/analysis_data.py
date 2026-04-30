import pandas as pd

df = pd.read_csv('data/processed/job_listings_clean.csv')

total_jobs = len(df)

print(f"\nTotal Jobs: {total_jobs}")

# ----------------------------
# Top Cities (with %)
# ----------------------------
print("\n=== TOP 10 HIRING CITIES ===")
city_counts = df['city'].value_counts().head(10)
city_pct = (city_counts / total_jobs * 100).round(2)

print(pd.DataFrame({
    'Count': city_counts,
    'Percentage (%)': city_pct
}))

# ----------------------------
# Jobs by Category
# ----------------------------
print("\n=== JOBS BY CATEGORY ===")
cat_counts = df['category'].value_counts()
cat_pct = (cat_counts / total_jobs * 100).round(2)

print(pd.DataFrame({
    'Count': cat_counts,
    'Percentage (%)': cat_pct
}))

# ----------------------------
# Top Companies (with %)
# ----------------------------
print("\n=== TOP 10 HIRING COMPANIES ===")
comp_counts = df['company'].value_counts().head(10)
comp_pct = (comp_counts / total_jobs * 100).round(2)

print(pd.DataFrame({
    'Count': comp_counts,
    'Percentage (%)': comp_pct
}))

# ----------------------------
# Keyword Distribution
# ----------------------------
print("\n=== JOBS BY SEARCH KEYWORD ===")
kw_counts = df['search_keyword'].value_counts()
kw_pct = (kw_counts / total_jobs * 100).round(2)

print(pd.DataFrame({
    'Count': kw_counts,
    'Percentage (%)': kw_pct
}))

# ----------------------------
# Monthly Trend
# ----------------------------
print("\n=== JOBS BY MONTH ===")
monthly_counts = df['month'].value_counts().sort_index()
monthly_pct = (monthly_counts / total_jobs * 100).round(2)

print(pd.DataFrame({
    'Count': monthly_counts,
    'Percentage (%)': monthly_pct
}))

# ----------------------------
# Key Insights (AUTO GENERATED)
# ----------------------------
top_city = df['city'].value_counts().idxmax()
top_city_pct = df['city'].value_counts(normalize=True).max() * 100

top_role = df['search_keyword'].value_counts().idxmax()
top_role_pct = df['search_keyword'].value_counts(normalize=True).max() * 100

print("\n=== KEY INSIGHTS ===")
print(f"- {top_city} accounts for {top_city_pct:.2f}% of all job listings")
print(f"- Most searched role: {top_role} ({top_role_pct:.2f}%)")
