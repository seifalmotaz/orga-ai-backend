"""Run the model interactively."""

import asyncio
from datetime import datetime
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import dotenv

# Load environment variables
dotenv.load_dotenv()

import asyncio  # noqa: E402, F811
from lmnr import Laminar  # noqa: E402
from langchain_core.messages import HumanMessage, SystemMessage  # noqa: E402
from src.lib.main import create_agent_graph  # noqa: E402
from langchain_core.runnables.config import RunnableConfig  # noqa: E402


# Initialize Laminar
Laminar.initialize(project_api_key=os.getenv("LMNR_API_KEY"))


async def main():
    app = create_agent_graph()
    user_config: RunnableConfig = {
        "configurable": {"thread_id": "123"},
    }

    # Load the system prompt **once** and send it only with the first user message
    with open("src/lib/prompts/system_prompt_template.md", "r") as file:
        system_prompt = file.read()

    first_interaction = True  # Flag to ensure the system prompt is sent only once

    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break

        # Build the message list, including the system prompt only once
        messages_to_send = []
        if first_interaction:
            messages_to_send.append(SystemMessage(content=system_prompt))
            messages_to_send.append(
                SystemMessage(
                    content=f"Current date: {datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}\nCurrent date ISO: {datetime.now().isoformat()}"
                )
            )
            first_interaction = False

        messages_to_send.append(HumanMessage(content=query))

        result = await app.ainvoke(
            {"messages": messages_to_send},
            config=user_config,
            stream_mode="values",
        )
        messages = result["messages"]
        # last message is the response
        response = messages[-1]
        print(response.content)
        print("-" * 100)


if __name__ == "__main__":
    asyncio.run(main())
