import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

if not app_id or not app_key:
    raise ValueError("Missing Adzuna credentials in .env")

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

params = {
    "app_id": app_id,
    "app_key": app_key,
    "what": "Java developer",
    "where": "Delhi",
    "results_per_page": 10,
    "content-type": "application/json",
}

response = requests.get(url, params=params, timeout=20)
print("HTTP status:", response.status_code)
response.raise_for_status()

data = response.json()

print("Total matching jobs:", data.get("count", "unknown"))

for job in data.get("results", []):
    print(f"\nTitle: {job.get('title')}")
    print(f"Company: {job.get('company', {}).get('display_name')}")
    print(f"Location: {job.get('location', {}).get('display_name')}")
    print(f"Link: {job.get('redirect_url')}")
