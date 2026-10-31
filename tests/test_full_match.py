from tools.parse_resume import parse_resume
from tools.analyze_job import extract_requirements
from tools.match_resume import match_resume

resume_text = parse_resume("data/resume.docx")

with open("data/job_description.txt", encoding="utf-8") as file:
    job_description = file.read()

requirements = extract_requirements(job_description)
result = match_resume(requirements, resume_text)

print("Match score:", result["match_score"], "%")
print("\nMatched required skills:")
for item in result["matched_skills"]:
    print(f"- {item['skill']} ({item['match_type']})")
    print("  Evidence:", item["evidence"])

print("\nMissing required skills:")
for skill in result["missing_required_skills"]:
    print("-", skill)

print("\nPreferred skills found:")
for item in result["preferred_skills_found"]:
    print(f"- {item['skill']} ({item['match_type']})")
