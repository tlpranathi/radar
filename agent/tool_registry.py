from google.genai import types
from tools.search_postings import search_postings
from tools.analyze_job import extract_requirements
from tools.research_company import research_company
from tools.parse_resume import parse_resume
from tools.match_resume import match_resume
from workflows.job_analysis import analyze_job_workflow

DEFAULT_RESUME_PATH = "data/resume.pdf"


def analyze_job(jd_text, company, role):
    return analyze_job_workflow(
        jd_text=jd_text,
        resume_path=DEFAULT_RESUME_PATH,
        company=company,
        role=role
    )

TOOLS = {
    "search_postings": search_postings,
    "extract_requirements": extract_requirements,
    "research_company": research_company,
    "parse_resume": parse_resume,
    "match_resume": match_resume,
    "analyze_job": analyze_job,
}

def execute_tool(tool_name, arguments):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool_function = TOOLS[tool_name]

    return tool_function(**arguments)


def get_available_tools():
    return list(TOOLS.keys())

def get_gemini_tools():
    search_postings_declaration = types.FunctionDeclaration(
        name="search_postings",
        description=(
            "Search for job and internship postings based on role, "
            "keywords, and location."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "role": types.Schema(
                    type=types.Type.STRING,
                    description="The job role to search for."
                ),
                "keywords": types.Schema(
                    type=types.Type.STRING,
                    description="Additional keywords to narrow the search."
                ),
                "location": types.Schema(
                    type=types.Type.STRING,
                    description="The location to search in."
                ),
                "results_per_page": types.Schema(
                    type=types.Type.INTEGER,
                    description="Number of job results to retrieve."
                )
            },
            required=["role"]
        )
    )

    search_tool = types.Tool(
        function_declarations=[search_postings_declaration]
    )
    
    analyze_job_declaration = types.FunctionDeclaration(
        name="analyze_job",
        description=(
            "Perform a complete analysis of a job description "
            "against the user's resume. Extract job requirements, "
            "match resume skills, research company interviews, "
            "and generate a personalized preparation plan. "
            "Use this when the user wants to analyze a specific job."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "jd_text": types.Schema(
                    type=types.Type.STRING,
                    description="The complete job description text."
                ),
                "company": types.Schema(
                    type=types.Type.STRING,
                    description="The company offering the job."
                ),
                "role": types.Schema(
                    type=types.Type.STRING,
                    description="The job role or position."
                )
            },
            required=["jd_text", "company", "role"]
        )
    )

    analyze_tool = types.Tool(
        function_declarations=[analyze_job_declaration]
    )

    return [search_tool, analyze_tool]
