"""Run the model interactively."""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import dotenv

# Load environment variables
dotenv.load_dotenv()


from lmnr import Laminar
from langchain_core.messages import HumanMessage
from src.tools.main import create_agent_graph
from langchain_core.runnables.config import RunnableConfig



# Initialize Laminar
Laminar.initialize(project_api_key=os.getenv("LMNR_API_KEY"))


if __name__ == "__main__":
    app = create_agent_graph()
    user_config: RunnableConfig = {
        "configurable": {"thread_id": "123"},
    }
    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break
        result = app.invoke({"messages": [HumanMessage(content=query)]}, config=user_config, stream_mode="values")
        messages = result["messages"]
        # last message is the response
        response = messages[-1]
        print(response.content)
        print("-" * 100)