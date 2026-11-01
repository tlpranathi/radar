from agent.react_agent import run_agent


goal = """
Find 5 Software Engineering Intern jobs in Bengaluru.

Use the search_postings tool to find actual job listings.

Choose the most relevant listing from the returned results.

Then use analyze_job to:
1. Extract its requirements.
2. Compare it against my resume.
3. Research the company's interview experiences.
4. Generate a personalized preparation plan.

Important:
- Only analyze a job returned by search_postings.
- Use the actual company name and job description.
- Do not invent job listings or job descriptions.
- If no suitable listings are returned, explain that.
- Clearly identify which job you selected.
"""

result = run_agent(goal, max_iterations=5)

print("\n========== RADAR JOB DISCOVERY ==========")
print(result)