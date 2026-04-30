import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")

def fetch_jobs(keyword, country='in', pages=5):
    """
    Fetch job listings from Adzuna API
    keyword: job title to search for
    country: 'in' for India, 'us' for USA, 'gb' for UK
    pages: number of pages to fetch (each page has 50 results)
    """
    all_jobs = []
    
    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
        
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'results_per_page': 50,
            'what': keyword,
            'content-type': 'application/json'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('results', [])
            all_jobs.extend(jobs)
            print(f"Page {page} fetched — {len(jobs)} jobs")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break
    
    return all_jobs

def parse_jobs(jobs):
    """Parse raw API response into a clean dataframe"""
    parsed = []
    
    for job in jobs:
        location_raw = job.get('location', {}).get('display_name', '')
        
        # Extract city (first part before comma)
        city = location_raw.split(',')[0] if location_raw else ''
        
        # Clean city
        if city in ['', 'India', None]:
            city = 'Not Specified'
        
        parsed.append({
            'title': job.get('title', ''),
            'company': job.get('company', {}).get('display_name', ''),
            'location': location_raw,
            'city': city,  # 👈 NEW COLUMN (important)
            'category': job.get('category', {}).get('label', ''),
            'salary_min': job.get('salary_min', None),
            'salary_max': job.get('salary_max', None),
            'contract_type': job.get('contract_type', ''),
            'created': job.get('created', ''),
            'description': job.get('description', ''),
            'url': job.get('redirect_url', '')
        })
    
    return pd.DataFrame(parsed)

if __name__ == "__main__":
    keywords = ["data analyst", "business analyst", "data scientist", "power bi", "sql analyst"]
    all_jobs = []
    
    for keyword in keywords:
        print(f"\nFetching {keyword} jobs...")
        jobs = fetch_jobs(keyword=keyword, country="in", pages=5)
        df_temp = parse_jobs(jobs)
        df_temp['search_keyword'] = keyword  # track which keyword fetched this
        all_jobs.append(df_temp)
    
    df_final = pd.concat(all_jobs, ignore_index=True)
    df_final.drop_duplicates(subset=['url'], inplace=True)  # remove duplicates
    
    print(f"\nTotal unique jobs fetched: {len(df_final)}")
    print(df_final.head())
    
    df_final.to_csv('data/raw/job_listings1.csv', index=False)
    print("\nData saved to data/raw/job_listings.csv")