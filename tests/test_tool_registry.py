from agent.tool_registry import get_available_tools, execute_tool

print("Available tools:")
print(get_available_tools())

print("\nTesting unknown tool:")

try:
    execute_tool("fake_tool", {})
except ValueError as error:
    print(error)
