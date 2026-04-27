# import asyncio
# import pandas as pd
# from playwright.async_api import async_playwright

# async def scrape_indeed(query="Data Analyst", location="India"):
#     async with async_playwright() as p:
#         # Launch browser
#         browser = await p.chromium.launch(headless=False)  # change to True if you don’t want UI
#         page = await browser.new_page()

#         # Build search URL
#         url = f"https://in.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
#         await page.goto(url)

#         # Wait for job cards to load
#         await page.wait_for_selector("div.job_seen_beacon")

#         jobs = []
#         job_cards = await page.query_selector_all("div.job_seen_beacon")

#         for job in job_cards[:10]:  # scrape only first 10 jobs
#             title = await job.query_selector("h2.jobTitle")
#             company = await job.query_selector("span.companyName")
#             location = await job.query_selector("div.companyLocation")

#             jobs.append({
#                 "title": await title.inner_text() if title else None,
#                 "company": await company.inner_text() if company else None,
#                 "location": await location.inner_text() if location else None
#             })

#         await browser.close()
#         return jobs

# # Run
# if __name__ == "__main__":
#     results = asyncio.run(scrape_indeed("Data Analyst", "Lucknow"))

#     # Save results to CSV
#     df = pd.DataFrame(results)
#     df.to_csv("indeed_jobs.csv", index=False, encoding="utf-8")

#     print("✅ Jobs saved to indeed_jobs.csv")

import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_indeed(query="Data Analyst", location="India"):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # change to True if you don’t want UI
        page = await browser.new_page()

        # Build search URL
        url = f"https://in.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
        await page.goto(url)

        # Wait for job cards to load
        await page.wait_for_selector("div.job_seen_beacon")

        jobs = []
        job_cards = await page.query_selector_all("div.job_seen_beacon")

        for job in job_cards[:10]:  # scrape only first 10 jobs
            title_el = await job.query_selector("h2.jobTitle span")
            company_el = await job.query_selector("span.companyName")
            location_el = await job.query_selector("div.companyLocation")
            salary_el = await job.query_selector("div.salary-snippet-container")

            title = await title_el.inner_text() if title_el else None
            company = await company_el.inner_text() if company_el else None
            loc = await location_el.inner_text() if location_el else None
            salary = await salary_el.inner_text() if salary_el else "Not disclosed"

            jobs.append({
                "title": title,
                "company": company,
                "location": loc,
                "salary": salary
            })

        await browser.close()
        return jobs

# Run
if __name__ == "__main__":
    results = asyncio.run(scrape_indeed("Business Analyst", "Lucknow"))

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv("indeed_jobs.csv", index=False, encoding="utf-8")

    print("✅ Jobs saved to indeed_jobs.csv")
