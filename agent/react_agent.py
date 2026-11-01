import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent.tool_registry import get_gemini_tools, execute_tool

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


def run_agent(user_goal, max_iterations=5):

    # validate user input
    if not isinstance(user_goal, str) or not user_goal.strip():
        raise ValueError("User goal must be a non-empty string")

    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool):
        raise ValueError("max_iterations must be an integer")

    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env")

    client = genai.Client(api_key=api_key)

    tools = get_gemini_tools()

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
                "Use available tools when necessary. "
                "Never invent tool results. "
                "If a tool fails, explain the problem honestly. "
                "Give a concise final response."
            )
        )
    )

    logger.info("Starting agent")
    response = chat.send_message(user_goal)

    # reAct loop
    for iteration in range(max_iterations + 1):

        function_calls = response.function_calls

        # gemini has finished
        if not function_calls:
            logger.info("Agent finished successfully")
            return response.text or "Agent finished without a text response."

        # do not execute more tools after reaching the limit
        if iteration == max_iterations:
            logger.warning("Maximum tool-call iterations reached")
            return (
                "Agent stopped: maximum number of tool-call "
                "iterations reached."
            )

        function_responses = []

        for function_call in function_calls:

            tool_name = function_call.name
            arguments = dict(function_call.args or {})

            logger.info(
                "Executing tool: %s | Arguments: %s",
                tool_name,
                arguments
            )

            try:
                result = execute_tool(tool_name, arguments)

                tool_result = {
                    "success": True,
                    "result": result
                }

                logger.info("Tool completed: %s", tool_name)

            except Exception as error:

                logger.exception("Tool failed: %s", tool_name)

                tool_result = {
                    "success": False,
                    "error": str(error)
                }

            function_responses.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response=tool_result
                )
            )

        # give Gemini the tool results
        response = chat.send_message(function_responses)

    return "Agent stopped unexpectedly."