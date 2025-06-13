from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from .tools_func import tools, tool_node
from .state import AgentState
from .models import gpt4dot1


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine whether to continue with tools or end the conversation."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"


def call_model(state: AgentState):
    """Call the model to generate a response."""
    messages = state["messages"]
    model = gpt4dot1.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}


# Create the graph
def create_agent_graph() -> CompiledStateGraph:
    """Create and compile the LangGraph agent."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint
    workflow.add_edge(START, "agent")

    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")

    # Add memory
    memory = MemorySaver()

    # Compile the graph
    app = workflow.compile(checkpointer=memory)

    return app
