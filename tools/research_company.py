import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def research_company(
    company: str,
    role: str,
    max_results: int = 5,
) -> list[dict]:
    """
    Search for relevant interview experiences and preparation
    resources for a particular company and role.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("Missing TAVILY_API_KEY in .env")

    if not isinstance(company, str) or not company.strip():
        raise ValueError("company must be a non-empty string")

    if not isinstance(role, str) or not role.strip():
        raise ValueError("role must be a non-empty string")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10")

    client = TavilyClient(api_key=api_key)

    # search 1: look for actual interview experiences.
    interview_query = (
        f'"{company}" "{role}" interview experience '
        "technical rounds coding questions"
    )

    # search 2: look for interview preparation and hiring information.
    preparation_query = (
        f"{company} {role} technical interview questions "
        "hiring process recruitment coding assessment"
    )

    trusted_domains = [
        "reddit.com",
        "glassdoor.com",
        "leetcode.com",
        "geeksforgeeks.org",
        "medium.com",
    ]

    search_results = []

    # search for interview experiences on relevant platforms.
    response = client.search(
        query=interview_query,
        max_results=max_results,
        search_depth="advanced",
        topic="general",
        include_domains=trusted_domains,
    )

    search_results.extend(response.get("results", []))

    # run a second, broader search for preparation resources.
    response = client.search(
        query=preparation_query,
        max_results=max_results,
        search_depth="advanced",
        topic="general",
    )

    search_results.extend(response.get("results", []))

    results = []
    seen_urls = set()

    relevant_keywords = [
        "interview",
        "intern",
        "internship",
        "hiring process",
        "technical round",
        "coding round",
        "recruitment",
        "coding assessment",
    ]

    for item in search_results:
        title = item.get("title") or ""
        content = item.get("content") or ""
        url = item.get("url")

        if not url or url in seen_urls:
            continue

        # ignore pages that do not appear relevant to interviews.
        combined_text = (title + " " + content).lower()

        if not any(
            keyword in combined_text
            for keyword in relevant_keywords
        ):
            continue

        seen_urls.add(url)

        results.append({
            "title": title,
            "url": url,
            "content": content,
            "score": item.get("score", 0),
        })

    # put higher-scoring search results first.
    results.sort(
        key=lambda item: item["score"] or 0,
        reverse=True,
    )

    return results[:max_results]
