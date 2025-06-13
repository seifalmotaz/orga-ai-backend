

import os
import dotenv
from lmnr import Laminar
from langchain_core.messages import HumanMessage
from src.tools.main import create_agent_graph

dotenv.load_dotenv()

Laminar.initialize(project_api_key=os.getenv("LMNR_API_KEY"))


if __name__ == "__main__":
    app = create_agent_graph()
    while True:
        query = input("Enter a query: ")
        if query.lower() == "exit":
            break
        app.invoke({"messages": [HumanMessage(content=query)]})