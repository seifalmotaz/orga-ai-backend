from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


# Define tools that our agent can use
@tool
def search_tool(query: str) -> str:
    """Search for information on the internet. Use this when you need to find current information about something."""
    # Simulate search results
    search_results = [
        f"Search result 1 for '{query}': This is a simulated search result about {query}.",
        f"Search result 2 for '{query}': Additional information about {query} can be found here.",
        f"Search result 3 for '{query}': More details about {query} from another source.",
    ]
    return "\n".join(search_results)


@tool
def calculator_tool(expression: str) -> str:
    """Calculate mathematical expressions. Use this for any math calculations."""
    try:
        # Simple calculator - only allow basic operations for security
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"

        result = eval(expression)
        return f"The result of {expression} is: {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"


@tool
def weather_tool(location: str) -> str:
    """Get weather information for a specific location."""
    # Simulate weather data
    import random  # Assuming random is needed here

    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "partly cloudy"]
    temp = random.randint(-10, 35)
    condition = random.choice(weather_conditions)
    return f"Weather in {location}: {condition}, {temp}°C"


@tool
def task_manager_tool(action: str, task: str = "") -> str:
    """Manage tasks - add, list, or complete tasks. Actions: 'add', 'list', 'complete'."""
    # Simulate a simple task manager
    if action == "add":
        return f"Task added: {task}"
    elif action == "list":
        return "Current tasks:\n1. Review project proposal\n2. Schedule team meeting\n3. Update documentation"
    elif action == "complete":
        return f"Task completed: {task}"
    else:
        return "Available actions: add, list, complete"


# Create the tools list
tools = [search_tool, calculator_tool, weather_tool, task_manager_tool]
# Create tool node
tool_node = ToolNode(tools)
