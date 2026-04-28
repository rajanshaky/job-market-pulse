import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def clean_jobs(filepath='data/raw/job_listings.csv'):
    df = pd.read_csv(filepath)
    
    print(f"Raw data shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # Clean title — remove extra whitespace
    df['title'] = df['title'].str.strip()
    
    # Clean company name
    df['company'] = df['company'].str.strip()
    
    # Extract city from location
    df['city'] = df['location'].str.split(',').str[0].str.strip()
    
    # Clean created date
    df['created'] = pd.to_datetime(df['created'])
    df['date'] = df['created'].dt.date
    df['month'] = df['created'].dt.month
    df['year'] = df['created'].dt.year
    
    # Fill missing salaries with 0
    df['salary_min'] = df['salary_min'].fillna(0)
    df['salary_max'] = df['salary_max'].fillna(0)
    
    # Add salary range column
    df['has_salary'] = df['salary_min'] > 0
    
    # Clean contract type
    df['contract_type'] = df['contract_type'].fillna('Not Specified')
    
    # Drop description and url for analysis
    df_clean = df.drop(columns=['description', 'url'])
    
    print(f"\nCleaned data shape: {df_clean.shape}")
    
    # Save cleaned data
    df_clean.to_csv('data/processed/job_listings_clean.csv', index=False)
    print("\nCleaned data saved to data/processed/job_listings_clean.csv")
    
    return df_clean

if __name__ == "__main__":
    df = clean_jobs()
    print(df.head())