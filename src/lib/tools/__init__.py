from datetime import date, datetime, timedelta
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from src.lib.tools.tasks_tools import (
    create_task,
    get_task_by_id,
    get_tasks_filtered,
    get_today_tasks,
)


@tool
def get_today_date_and_time() -> dict:
    """Get the current date and time.
    Return:
    - date: The current date.
    - time: The current time.
    - day: The current day of the week.
    - month: The current month.
    - year: The current year.
    """
    return {
        "date": date.today().isoformat(),
        "time": datetime.now().isoformat(),
        "day": date.today().strftime("%A"),
        "month": date.today().strftime("%B"),
        "year": date.today().strftime("%Y"),
    }


@tool
def get_day_after(
    after_months: Annotated[int, "The number of months to add to the current date"],
    after_weeks: Annotated[int, "The number of weeks to add to the current date"],
    after_days: Annotated[int, "The number of days to add to the current date"],
    after_hours: Annotated[int, "The number of hours to add to the current date"],
    after_minutes: Annotated[int, "The number of minutes to add to the current date"],
    after_seconds: Annotated[int, "The number of seconds to add to the current date"],
) -> dict:
    """Get the date and time after the given number of months, days, hours, minutes, and seconds.
    Return:
    - date: The current date.
    - time: The current time.
    - day: The current day of the week.
    - month: The current month.
    - year: The current year.
    """
    if after_months:
        after_weeks = (after_months * 4) + after_weeks
    date_to_return = date.today() + timedelta(
        weeks=after_weeks,
        days=after_days,
        hours=after_hours,
        minutes=after_minutes,
        seconds=after_seconds,
    )
    return {
        "date": date_to_return.isoformat(),
        "time": datetime.now().isoformat(),
        "day": date_to_return.strftime("%A"),
        "month": date_to_return.strftime("%B"),
        "year": date_to_return.strftime("%Y"),
    }


# Create the tools list
tools = [
    get_today_date_and_time,
    get_day_after,
    get_today_tasks,
    get_tasks_filtered,
    create_task,
    get_task_by_id,
]
# Create tool node
tool_node = ToolNode(tools)
