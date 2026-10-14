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
    Search the web for interview experiences and preparation
    resources for a company and role.
    """
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("Missing TAVILY_API_KEY in .env")

    if not company.strip():
        raise ValueError("company cannot be empty")

    if not role.strip():
        raise ValueError("role cannot be empty")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10")

    client = TavilyClient(api_key=api_key)

    query = (
        f"{company} {role} interview experience "
        "interview questions hiring process preparation"
    )

    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
        topic="general",
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content"),
            "score": item.get("score"),
        })

    return results
