from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
import time

driver_path = r"C:\Users\Rajan\Downloads\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

# options = Options()
# options.binary_location = r"C:\Users\Rajan\AppData\Local\Programs\Opera GX\opera.exe"

driver = webdriver.Chrome(service=service)

URL = "https://www.indeed.com/jobs?q=Data+Analyst&l=Lucknow"
driver.get(URL)

time.sleep(5)

jobs = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

for job in jobs:
    title = job.find_element(By.CLASS_NAME, "jobTitle").text if job.find_elements(By.CLASS_NAME, "jobTitle") else "N/A"
    company = job.find_element(By.CLASS_NAME, "companyName").text if job.find_elements(By.CLASS_NAME, "companyName") else "N/A"
    location = job.find_element(By.CLASS_NAME, "companyLocation").text if job.find_elements(By.CLASS_NAME, "companyLocation") else "N/A"

    print(f"Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print("-" * 40)

# print(driver.title)

driver.quit() 