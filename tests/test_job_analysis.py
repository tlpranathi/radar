from workflows.job_analysis import analyze_job_workflow


# read the job description
with open("data/job_description.txt", "r") as file:
    jd_text = file.read()

result = analyze_job_workflow(
    jd_text=jd_text,
    resume_path="data/resume.pdf",
    company="Google",
    role="Software Engineering Intern",
)

print("\n========== JOB ANALYSIS ==========")

print("\nCompany:", result["company"])
print("Role:", result["role"])

print("\nRequirements:")
print(result["requirements"])

print("\nResume Match:")
print(result["resume_match"])

print("\nInterview Research:")
for item in result["interview_research"]:
    print("\nTitle:", item["title"])
    print("URL:", item["url"])
