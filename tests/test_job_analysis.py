from workflows.job_analysis import analyze_job_workflow
from workflows.display_report import display_job_report


with open("data/job_description.txt", "r") as file:
    jd_text = file.read()


result = analyze_job_workflow(
    jd_text=jd_text,
    resume_path="data/resume.pdf",
    company="Google",
    role="Software Engineering Intern",
)

display_job_report(result)