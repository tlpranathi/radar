import os
from dotenv import load_dotenv
from google import genai

from agent.tool_registry import get_gemini_tools

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=api_key)

tools = get_gemini_tools()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=(
        "Find Software Engineering Intern jobs "
        "in Bengaluru. Use the available tool."
    ),
    config={
        "tools": tools,
        "tool_config": {
            "function_calling_config": {
                "mode": "ANY"
            }
        }
    }
)

print("Gemini response:")

if response.function_calls:
    for function_call in response.function_calls:
        print("Function:", function_call.name)
        print("Arguments:", function_call.args)
else:
    print(response.text)