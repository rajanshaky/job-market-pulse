import pandas as pd
import sqlalchemy as sal
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = "root"
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = "localhost"
PORT = "3306"
DATABASE = "job_market"

# Create database engine
engine = sal.create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# Test connection
with engine.connect() as connection:
    print("Connected to MySQL successfully!")

# Load cleaned data
df = pd.read_csv('data/processed/job_listings_clean.csv')
print(f"Loaded {len(df)} rows")

# Push to MySQL
df.to_sql('job_listings', con=engine, index=False, if_exists='replace')
print("Data loaded into MySQL successfully!")