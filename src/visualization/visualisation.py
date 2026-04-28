import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/processed/job_listings_clean.csv')
plt.style.use('seaborn-v0_8')

# 1. Top 10 Hiring Cities
plt.figure(figsize=(10,6))
city_counts = df['city'].value_counts().head(10)
sns.barplot(x=city_counts.values, y=city_counts.index, palette='viridis')
plt.title('Top 10 Hiring Cities for Data Roles in India')
plt.xlabel('Number of Job Postings')
plt.tight_layout()
plt.savefig('data/processed/top_cities.png', dpi=150, bbox_inches='tight')
plt.show()

# 2. Jobs by Search Keyword
plt.figure(figsize=(8,5))
keyword_counts = df['search_keyword'].value_counts()
sns.barplot(x=keyword_counts.values, y=keyword_counts.index, palette='coolwarm')
plt.title('Job Postings by Role Type')
plt.xlabel('Number of Postings')
plt.tight_layout()
plt.savefig('data/processed/jobs_by_keyword.png', dpi=150, bbox_inches='tight')
plt.show()

# 3. Top 10 Hiring Companies
plt.figure(figsize=(10,6))
company_counts = df['company'].value_counts().head(10)
sns.barplot(x=company_counts.values, y=company_counts.index, palette='magma')
plt.title('Top 10 Hiring Companies for Data Roles')
plt.xlabel('Number of Job Postings')
plt.tight_layout()
plt.savefig('data/processed/top_companies.png', dpi=150, bbox_inches='tight')
plt.show()

# 4. Jobs by Category
plt.figure(figsize=(10,6))
cat_counts = df['category'].value_counts().head(8)
sns.barplot(x=cat_counts.values, y=cat_counts.index, palette='Blues_r')
plt.title('Job Postings by Category')
plt.xlabel('Number of Postings')
plt.tight_layout()
plt.savefig('data/processed/jobs_by_category.png', dpi=150, bbox_inches='tight')
plt.show()

# 5. Monthly Posting Trend
plt.figure(figsize=(12,5))
monthly = df['month'].value_counts().sort_index()
plt.plot(monthly.index, monthly.values, marker='o', color='steelblue')
plt.title('Job Postings by Month')
plt.xlabel('Month')
plt.ylabel('Number of Postings')
plt.xticks(range(1,13), ['Jan','Feb','Mar','Apr','May','Jun',
                          'Jul','Aug','Sep','Oct','Nov','Dec'])
plt.tight_layout()
plt.savefig('data/processed/monthly_trend.png', dpi=150, bbox_inches='tight')
plt.show()
