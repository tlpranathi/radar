import os
import json
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

class WeeklyPlan(BaseModel):
    week: int
    focus: str
    objectives: list[str] = Field(min_length=1)


class PreparationPlan(BaseModel):
    priority_gaps: list[str]
    study_topics: list[str]
    practice_tasks: list[str]
    interview_tips: list[str]
    weekly_plan: list[WeeklyPlan]

def generate_prep_plan(requirements, resume_match, interview_research):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are Radar, an interview preparation assistant.

    Generate a personalized interview preparation plan
    using the following information.

    JOB REQUIREMENTS:
    {json.dumps(requirements, indent=2)}

    RESUME MATCH:
    {json.dumps(resume_match, indent=2)}

    INTERVIEW RESEARCH:
    {json.dumps(interview_research, indent=2)}

    Instructions:

    1. Identify the most important missing skills.
    2. Prioritize skills based on the job requirements.
    3. Suggest specific topics to study.
    4. Suggest practical exercises or coding problems.
    5. Use the interview research to identify useful
       interview preparation areas.
    6. Do not invent interview questions or claim that
       a topic was asked by the company unless the
       research supports that claim.
    7. Keep the plan realistic for a student.

    Return valid JSON with this structure:

    {{
        "priority_gaps": [],
        "study_topics": [],
        "practice_tasks": [],
        "interview_tips": [],
        "weekly_plan": []
    }}
    """

    response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PreparationPlan,
    )
)

    try:
        plan = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        raise ValueError("Gemini returned invalid preparation plan JSON")

    if not isinstance(plan, dict):
        raise ValueError("Preparation plan must be a JSON object")

    return plan
