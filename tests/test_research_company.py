from tools.research_company import research_company

results = research_company(
    company="Google",
    role="Software Engineering Intern",
    max_results=5,
)

print(f"Found {len(results)} research results.")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Title:", result["title"])
    print("URL:", result["url"])
    print("Content:", (result["content"] or "")[:400])
