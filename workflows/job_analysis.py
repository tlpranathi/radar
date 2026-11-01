from tools.analyze_job import extract_requirements
from tools.parse_resume import parse_resume
from tools.match_resume import match_resume
from tools.research_company import research_company


def analyze_job_workflow(jd_text, resume_path, company, role):
    """
    Analyze a job description against a resume and
    research interview preparation resources.
    """

    if not jd_text or not jd_text.strip():
        raise ValueError("Job description cannot be empty")

    if not resume_path or not resume_path.strip():
        raise ValueError("Resume path cannot be empty")

    if not company or not company.strip():
        raise ValueError("Company cannot be empty")

    if not role or not role.strip():
        raise ValueError("Role cannot be empty")

    # step 1: extract requirements from the job description
    print("\n[1/4] Extracting job requirements...")
    requirements = extract_requirements(jd_text)

    # step 2: extract text from the resume
    print("\n[2/4] Parsing resume...")
    resume_text = parse_resume(resume_path)

    # step 3: compare resume with job requirements
    print("\n[3/4] Matching resume against requirements...")
    resume_match = match_resume(requirements, resume_text)

    # step 4: research company interview experiences
    print("\n[4/4] Researching company interviews...")
    interview_research = research_company(company, role)

    # combine all results
    return {
        "company": company,
        "role": role,
        "requirements": requirements,
        "resume_match": resume_match,
        "interview_research": interview_research,
    }
