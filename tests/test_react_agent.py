from agent.react_agent import run_agent

goal = (
    "Find Software Engineering Intern jobs "
    "in Bengaluru. Search for 5 results and summarize them."
)

result = run_agent(goal)

print("\nFinal Agent Response:")
print(result)