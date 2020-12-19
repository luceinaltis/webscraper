import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def extaract_indeed_pages():
    indeed_result = requests.get(URL)

    indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

    pagination = indeed_soup.find("div", {"class": "pagination"})

    pages = pagination.find_all("span", {"class": "pn"})
    spans = []
    for page in pages[:-1]:
        spans.append(int(page.string))

    max_page = spans[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]

    return {"title": title, "company": company, "location": location, "link": f"https://indeed.com/viewjob?jk={job_id}"}


def extract_indeed_jobs(last_pages):
    jobs = []

    for page in range(last_pages):
        print(f"Indeed 긁어오는중 {page} of {last_pages}")
        res = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    max_indeed_pages = extaract_indeed_pages()

    jobs = extract_indeed_jobs(max_indeed_pages)

    return jobs
