import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.tool_registry import get_gemini_tools, execute_tool


load_dotenv()

MODEL = "gemini-3.5-flash-lite"


def run_agent(user_goal, max_iterations=5):

    if not user_goal or not user_goal.strip():
        raise ValueError("User goal cannot be empty")

    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env")

    client = genai.Client(api_key=api_key)

    # give Gemini access to Radar's registered tools
    tools = get_gemini_tools()

    # create a conversation with Gemini
    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            tools=tools,
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode="AUTO"
                )
            ),
            system_instruction=(
                "You are Radar, a job discovery and preparation agent. "
                "Use available tools when necessary to accomplish the "
                "user's goal. Do not invent tool results. "
                "Give a concise final response."
            )
        )
    )

    # send the initial user goal
    response = chat.send_message(user_goal)

    # reAct loop
    for iteration in range(max_iterations):

        function_calls = response.function_calls

        # no function calls means Gemini is ready with its answer
        if not function_calls:
            return response.text

        function_responses = []

        # execute every function requested by Gemini
        for function_call in function_calls:

            print(f"\nExecuting tool: {function_call.name}")
            print(f"Arguments: {function_call.args}")

            try:
                result = execute_tool(
                    function_call.name,
                    dict(function_call.args or {})
                )

            except Exception as error:
                result = {"error": str(error)}

            # convert the Python result into a Gemini function response
            function_responses.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result}
                )
            )

        # send the tool results back to Gemini
        response = chat.send_message(function_responses)

    return "Agent stopped: maximum number of iterations reached."