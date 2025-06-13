from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
import operator


# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
