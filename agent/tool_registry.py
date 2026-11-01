from google.genai import types
from tools.search_postings import search_postings
from tools.analyze_job import extract_requirements
from tools.research_company import research_company
from tools.parse_resume import parse_resume
from tools.match_resume import match_resume

TOOLS = {
    "search_postings": search_postings,
    "extract_requirements": extract_requirements,
    "research_company": research_company,
    "parse_resume": parse_resume,
    "match_resume": match_resume
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

    return [search_tool]