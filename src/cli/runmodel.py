"""Run the model interactively."""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import dotenv

# Load environment variables
dotenv.load_dotenv()

import asyncio  # noqa: E402, F811
from lmnr import Laminar  # noqa: E402
from langchain_core.messages import HumanMessage  # noqa: E402
from src.lib.main import create_agent_graph  # noqa: E402
from langchain_core.runnables.config import RunnableConfig  # noqa: E402


# Initialize Laminar
Laminar.initialize(project_api_key=os.getenv("LMNR_API_KEY"))


async def main():
    app = create_agent_graph()
    user_config: RunnableConfig = {
        "configurable": {"thread_id": "123"},
    }
    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break
        result = await app.ainvoke(
            {"messages": [HumanMessage(content=query)]},
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
