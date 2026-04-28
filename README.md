# Job Market Pulse — Live Job Market Analysis

An end-to-end data analytics project that fetches live job listings 
from the Adzuna API, processes them through a full pipeline, and 
visualizes insights about the Indian data job market.

## Project Pipeline
Adzuna API → Python (Ingestion) → Cleaning → Analysis → Visualization

## Project Structure
job_market_pulse/
├── data/
│   ├── raw/              # Raw data from API (gitignored)
│   └── processed/        # Cleaned data (gitignored)
├── notebooks/
│   └── analysis.ipynb    # Full analysis with inline charts
├── src/
│   ├── analysis/
│   │   └── analysis_data.py
│   ├── cleaning/
│   │   └── clean_data.py
│   └── visualization/
│       └── visualisation.py
├── data_ingestion.py     # Fetches data from Adzuna API
├── .gitignore
└── README.md

## Tools Used
- Python (Pandas, Matplotlib, Seaborn, Requests, python-dotenv)
- Adzuna API
- Jupyter Notebook

## Key Findings
| Insight | Finding |
|---|---|
| 🏙️ Top City | Bangalore (336 jobs) |
| 🔍 Most In-Demand Role | Data Analyst / Business Analyst (tied at 250) |
| 🏢 Top Hiring Company | Tata Consultancy Services (43 jobs) |
| 📂 Dominant Category | IT Jobs (87% of all postings) |
| 📊 Total Jobs Analyzed | 1,149 live job listings |

## Setup
1. Clone the repo

2. Install dependencies:  
                          pip install pandas matplotlib seaborn requests python-dotenv

3. Create a `.env` file:
                          ADZUNA_APP_ID=your_app_id
                          ADZUNA_APP_KEY=your_app_key

4. Run pipeline in order: 
                          python data_ingestion.py
                          python src/cleaning/clean_data.py
                          python src/analysis/analysis_data.py
                          python src/visualization/visualisation.py

5. Open `notebooks/analysis.ipynb` for full analysis

## API
Data sourced from [Adzuna API](https://developer.adzuna.com) — a legal and free job listings API.