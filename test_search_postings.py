from tools.search_postings import search_postings

def is_internship_listing(job: dict) -> bool:
    """Check whether the returned job text mentions internship terms."""
    text = " ".join([
        job.get("title") or "",
        job.get("description") or "",
    ]).lower()

    return "intern" in text or "internship" in text

for keyword in ["intern", "internship"]:
    print(f"\n{'=' * 50}")
    print(f"Searching for: {keyword}")
    print("=" * 50)

    jobs = search_postings(
        role="software developer",
        keywords=keyword,
        location="Bengaluru",
        results_per_page=10,
    )

    relevant = [job for job in jobs if is_internship_listing(job)]

    print(f"Returned by Adzuna: {len(jobs)}")
    print(f"Matching internship terms: {len(relevant)}")

    for job in jobs:
        marker = "MATCH" if is_internship_listing(job) else "CHECK"
        print(f"\n[{marker}] {job['title']} — {job['company']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")
