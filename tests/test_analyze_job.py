from tools.analyze_job import extract_requirements

sample_jd = """
Software Engineering Intern

Requirements:
- Knowledge of Python and SQL
- Familiarity with Git
- Currently pursuing a degree in Computer Science or a related field

Preferred:
- Experience with Docker

Responsibilities:
- Develop and test backend services
- Write automated tests
"""

requirements = extract_requirements(sample_jd)

print("Extracted requirements:")
for field, value in requirements.items():
    print(f"\n{field}: {value}")

# basic validation checks
assert isinstance(requirements["required_skills"], list)
assert isinstance(requirements["preferred_skills"], list)
assert isinstance(requirements["responsibilities"], list)

print("\nSUCCESS: Structured job requirements extracted!")
