import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def clean_jobs(filepath='data/raw/job_listings1.csv'):
    df = pd.read_csv(filepath)
    
    print(f"Raw data shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # ----------------------------
    # Basic Cleaning
    # ----------------------------
    df['title'] = df['title'].astype(str).str.strip()
    df['company'] = df['company'].astype(str).str.strip().str.title()
    
    # ----------------------------
    # City Extraction & Cleaning
    # ----------------------------
    df['city'] = df['location'].astype(str).str.split(',').str[0].str.strip()
    
    # Replace invalid / missing values
    df['city'] = df['city'].replace(['', 'India', 'None', 'nan'], 'Not Specified')
    
    # Normalize city names
    df['city'] = df['city'].replace({
        'New Delhi': 'Delhi',
        'Bengaluru': 'Bangalore',
        'Navi Mumbai': 'Mumbai'
    })
    
    # ----------------------------
    # Date Processing
    # ----------------------------
    df['created'] = pd.to_datetime(df['created'], errors='coerce')
    df['date'] = df['created'].dt.date
    df['month'] = df['created'].dt.month
    df['year'] = df['created'].dt.year
    
    # ----------------------------
    # Salary Handling
    # ----------------------------
    df['has_salary'] = df['salary_min'].notna()
    df['salary_min'] = df['salary_min'].fillna(0)
    df['salary_max'] = df['salary_max'].fillna(0)
    
    # ----------------------------
    # Contract Type Cleaning
    # ----------------------------
    df['contract_type'] = df['contract_type'].fillna('Not Specified')
    
    # ----------------------------
    # Final Dataset (drop unnecessary columns)
    # ----------------------------
    df_clean = df.drop(columns=['description', 'url'])
    
    print(f"\nCleaned data shape: {df_clean.shape}")
    
    # ----------------------------
    # Validation Checks
    # ----------------------------
    print("\nTop cities:\n", df_clean['city'].value_counts().head(10))
    
    missing_pct = (df_clean['city'] == 'Not Specified').mean() * 100
    print(f"\nMissing city data: {missing_pct:.2f}%")
    
    # ----------------------------
    # Save Cleaned Data
    # ----------------------------
    output_path = 'data/processed/job_listings_clean.csv'
    df_clean.to_csv(output_path, index=False)
    
    print(f"\nCleaned data saved to {output_path}")
    
    return df_clean


if __name__ == "__main__":
    df = clean_jobs()
    print("\nPreview:\n", df.head())