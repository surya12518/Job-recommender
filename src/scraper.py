import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_remoteok(job_search: str, output_path="data/jobs.csv"):
    Job_search = '-'.join(job_search.strip().lower().split())
    url = f"https://remoteok.com/remote-{Job_search}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    jobs_list = []

    for job in soup.select("tr.job"):
        title_elem = job.select_one("h2")
        company_elem = job.select_one(".companyLink")
        location_elem = job.select_one(".location")
        link_elem = job.select_one("a.preventLink")
        desc_elem = job.select_one(".description")

        title = title_elem.get_text(strip=True) if title_elem else None
        company = company_elem.get_text(strip=True) if company_elem else None
        location = location_elem.get_text(strip=True) if location_elem else "Remote"
        posted_date = datetime.today().strftime("%Y-%m-%d")
        description = desc_elem.get_text(strip=True) if desc_elem else "No description provided."
        apply_url = "https://remoteok.com" + link_elem["href"] if link_elem else None

        if title and company and apply_url:
            jobs_list.append({
                "id": len(jobs_list) + 1,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "posted_date": posted_date,
                "apply_url": apply_url
            })

    df = pd.DataFrame(jobs_list)
    df.to_csv(output_path, index=False)
    print(f"✅ Scraped {len(df)} jobs for '{job_search}' → saved to {output_path}")
    return df
