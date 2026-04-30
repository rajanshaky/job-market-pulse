import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/processed/job_listings_clean.csv')
plt.style.use('seaborn-v0_8')

# Helper function (reduces repetition)
def plot_bar(data, title, xlabel, filename, color_palette):
    plt.figure(figsize=(10,6))
    sns.barplot(x=data.values, y=data.index, palette=color_palette)
    
    # Add labels
    for i, v in enumerate(data.values):
        plt.text(v, i, f' {v}', va='center')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(f'data/processed/{filename}', dpi=150, bbox_inches='tight')
    plt.show()


# ----------------------------
# 1. Top Cities (exclude Not Specified optionally)
# ----------------------------
city_counts = df[df['city'] != 'Not Specified']['city'].value_counts().head(10)
plot_bar(
    city_counts,
    'Top Hiring Cities (Excluding Unspecified Locations)',
    'Number of Job Postings',
    'top_cities.png',
    'viridis'
)


# ----------------------------
# 2. Jobs by Role
# ----------------------------
keyword_counts = df['search_keyword'].value_counts()
plot_bar(
    keyword_counts,
    'Distribution of Job Roles (BA leads demand)',
    'Number of Postings',
    'jobs_by_keyword.png',
    'coolwarm'
)


# ----------------------------
# 3. Top Companies
# ----------------------------
company_counts = df['company'].value_counts().head(10)
plot_bar(
    company_counts,
    'Top Hiring Companies (Few firms dominate hiring)',
    'Number of Job Postings',
    'top_companies.png',
    'magma'
)


# ----------------------------
# 4. Categories
# ----------------------------
cat_counts = df['category'].value_counts().head(8)
plot_bar(
    cat_counts,
    'Job Distribution by Category',
    'Number of Postings',
    'jobs_by_category.png',
    'Blues_r'
)


# ----------------------------
# 5. Monthly Trend
# ----------------------------
plt.figure(figsize=(12,5))
monthly = df['month'].value_counts().sort_index()

plt.plot(monthly.index, monthly.values, marker='o')

# annotate points
for x, y in zip(monthly.index, monthly.values):
    plt.text(x, y, str(y), ha='center', va='bottom')

plt.title('Monthly Job Posting Trend')
plt.xlabel('Month')
plt.ylabel('Number of Postings')
plt.xticks(range(1,13), ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'])

plt.tight_layout()
plt.savefig('data/processed/monthly_trend.png', dpi=150, bbox_inches='tight')
plt.show()