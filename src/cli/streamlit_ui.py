"""Streamlit UI for interacting with the LLM agent and visualizing the graph flow."""

import os
import sys
import streamlit as st
import json
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import dotenv

# Load environment variables
dotenv.load_dotenv()

from lmnr import Laminar
from langchain_core.messages import HumanMessage, AIMessage
from src.tools.main import create_agent_graph
from langchain_core.runnables.config import RunnableConfig


# Initialize Laminar
Laminar.initialize(project_api_key=os.getenv("LMNR_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Orga-AI Chat Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_graph" not in st.session_state:
    st.session_state.agent_graph = create_agent_graph()
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit_session"

def get_mermaid_diagram():
    """Get the Mermaid diagram representation of the agent graph."""
    try:
        return st.session_state.agent_graph.get_graph().draw_mermaid()
    except Exception as e:
        return f"Error generating diagram: {str(e)}"

def display_graph_visualization():
    """Display the LangGraph visualization using Mermaid."""
    st.subheader("🔄 Agent Graph Flow")
    
    mermaid_code = get_mermaid_diagram()
    
    # Display the mermaid diagram
    st.code(mermaid_code, language="mermaid")
    
    # Try to render the diagram if possible
    try:
        st.markdown(f"""
        ```mermaid
        {mermaid_code}
        ```
        """)
    except:
        st.info("Mermaid diagram code is shown above. You can copy it to visualize in a Mermaid viewer.")

def send_message_to_agent(user_input: str):
    """Send a message to the agent and get the response."""
    try:
        user_config: RunnableConfig = {
            "configurable": {"thread_id": st.session_state.thread_id},
        }

        # Create human message
        human_message = HumanMessage(content=user_input)

        # Get response from agent
        with st.spinner("🤖 Agent is thinking..."):
            result = st.session_state.agent_graph.invoke(
                {"messages": [human_message]},
                config=user_config
            )

        # Extract the response
        messages = result["messages"]
        ai_response = messages[-1]

        return ai_response.content

    except Exception as e:
        st.error(f"Error communicating with agent: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def stream_message_to_agent(user_input: str):
    """Send a message to the agent with streaming response."""
    try:
        user_config: RunnableConfig = {
            "configurable": {"thread_id": st.session_state.thread_id},
        }

        # Create human message
        human_message = HumanMessage(content=user_input)

        # Stream response from agent
        response_placeholder = st.empty()
        full_response = ""

        for chunk in st.session_state.agent_graph.stream(
            {"messages": [human_message]},
            config=user_config,
            stream_mode="values"
        ):
            if "messages" in chunk and chunk["messages"]:
                latest_message = chunk["messages"][-1]
                if hasattr(latest_message, 'content') and latest_message.content:
                    full_response = latest_message.content
                    response_placeholder.markdown(full_response)

        return full_response

    except Exception as e:
        st.error(f"Error streaming from agent: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main Streamlit application."""

    # Header
    st.title("🤖 Orga-AI Chat Interface")
    st.markdown("Welcome to the Orga-AI chat interface! This tool allows you to interact with the LLM agent and visualize the graph flow.")

    # Quick start examples
    with st.expander("💡 Quick Start Examples"):
        st.markdown("""
        **Try these example prompts:**
        - "Hello, how can you help me?"
        - "Search for information about Python programming"
        - "What tools do you have available?"
        - "Help me organize my tasks"
        """)

    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")

        # Clear conversation button
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.session_state.thread_id = f"streamlit_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.rerun()

        # Thread ID display
        st.text_input("Thread ID", value=st.session_state.thread_id, disabled=True)

        # Streaming toggle
        use_streaming = st.checkbox("🌊 Enable Streaming", value=False,
                                   help="Stream responses in real-time")

        # Agent info
        st.subheader("📊 Agent Info")
        st.info(f"Messages in conversation: {len(st.session_state.messages)}")

        # Environment info
        st.subheader("🔧 Environment")
        st.text(f"LMNR API Key: {'✅ Set' if os.getenv('LMNR_API_KEY') else '❌ Missing'}")
        st.text(f"OpenAI API Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")

        # Graph visualization toggle
        show_graph = st.checkbox("Show Graph Visualization", value=True)
    
    # Main content area
    if show_graph:
        col1, col2 = st.columns([2, 1])
    else:
        col1 = st.container()
        col2 = None
    
    with col1:
        st.subheader("💬 Conversation")
        
        # Display conversation history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to conversation
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                if use_streaming:
                    response = stream_message_to_agent(prompt)
                else:
                    response = send_message_to_agent(prompt)
                    st.markdown(response)

            # Add AI response to conversation
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Rerun to update the interface
            st.rerun()
    
    # Graph visualization column
    if show_graph and col2 is not None:
        with col2:
            display_graph_visualization()

if __name__ == "__main__":
    main()
