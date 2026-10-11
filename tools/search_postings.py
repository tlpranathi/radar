import os
import requests
from dotenv import load_dotenv

load_dotenv()

ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"


def search_postings(
    role: str,
    keywords: str = "",
    location: str = "Bengaluru",
    results_per_page: int = 10,
) -> list[dict]:
    """ Search Adzuna for jobs matching a role and extra keywords. """
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key: raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env")

    if not role.strip():
        raise ValueError("role cannot be empty")

    if not 1 <= results_per_page <= 50:
        raise ValueError("results_per_page must be between 1 and 50")

    # combine the role and optional keywords into one search query.
    query = " ".join(part.strip() for part in (role, keywords) if part.strip())

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    response = requests.get(ADZUNA_URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "description": job.get("description"),
            "url": job.get("redirect_url"),
            "created": job.get("created"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
        })

    return jobs
