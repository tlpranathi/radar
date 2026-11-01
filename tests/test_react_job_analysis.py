from pathlib import Path
from agent.react_agent import run_agent


# load the job description
jd_text = Path("data/job_description.txt").read_text()

# give Radar a goal
goal = f"""
Analyze this Google Software Engineering Intern position
against my resume.

Use the analyze_job tool to:
1. Extract the job requirements.
2. Compare them against my resume.
3. Research Google interview experiences.
4. Generate a personalized preparation plan.

Company: TechNova Solutions
Role: Software Engineering Intern

Here is the job description:

{jd_text}
"""

# run the ReAct agent
result = run_agent(goal, max_iterations=3)

print("\n========== RADAR AGENT RESPONSE ==========")
print(result)
