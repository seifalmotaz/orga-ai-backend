from datetime import date, datetime, time
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from src.lib.tools.tasks import create_task, get_today_tasks


@tool
def check_date_and_time(date: date, time: time) -> str:
    """Check if the date and time are in the past or future."""
    if date < datetime.now().date():
        return "Error: Date is in the past"
    return "Date is in the future"


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
tools = [
    calculator_tool,
    weather_tool,
    get_today_tasks,
    create_task,
    check_date_and_time,
]
# Create tool node
tool_node = ToolNode(tools)
