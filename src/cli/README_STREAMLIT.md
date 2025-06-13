# Streamlit UI for Orga-AI

This is a simple Streamlit-based user interface for interacting with the Orga-AI LLM agent and visualizing the LangGraph flow.

## Features

- **💬 Interactive Chat Interface**: Send messages to the LLM agent and see responses in real-time
- **🔄 Graph Visualization**: View the LangGraph agent flow using Mermaid diagrams
- **🌊 Streaming Support**: Enable streaming responses for real-time interaction
- **📊 Session Management**: Track conversation history and manage chat sessions
- **🔧 Environment Monitoring**: Check API key status and configuration

## Quick Start

### 1. Install Dependencies

Streamlit is already added to the dev dependencies. If you need to install it manually:

```bash
uv add --dev streamlit
```

### 2. Run the Streamlit UI

```bash
# Using the Makefile
make streamlit

# Or directly
uv run streamlit run src/cli/streamlit_ui.py
```

### 3. Open in Browser

The UI will be available at: http://localhost:8501

## Usage

### Basic Chat
1. Type your message in the chat input at the bottom
2. Press Enter or click Send
3. Watch the agent respond with the answer

### Example Prompts
- "Hello, how can you help me?"
- "Search for information about Python programming"
- "What tools do you have available?"
- "Help me organize my tasks"

### Features

#### Sidebar Controls
- **Clear Conversation**: Reset the chat history and start fresh
- **Thread ID**: View the current conversation thread identifier
- **Streaming Toggle**: Enable/disable real-time streaming responses
- **Environment Status**: Check if API keys are properly configured
- **Graph Visualization**: Toggle the Mermaid diagram display

#### Graph Visualization
The right panel shows the LangGraph agent flow as a Mermaid diagram. This helps you understand:
- How the agent processes messages
- The flow between different nodes (agent, tools)
- The decision points in the conversation

## Configuration

### Environment Variables
Make sure these are set in your `.env` file:

```bash
LMNR_API_KEY=your_laminar_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Customization
You can modify the UI by editing `src/cli/streamlit_ui.py`:
- Change the page layout
- Add new sidebar controls
- Modify the chat interface
- Customize the graph visualization

## Troubleshooting

### Common Issues

1. **"Error communicating with agent"**
   - Check that your API keys are set correctly
   - Ensure the agent graph is properly initialized

2. **Graph visualization not showing**
   - The Mermaid diagram should display as code
   - Copy the code to an external Mermaid viewer if needed

3. **Streaming not working**
   - Try disabling streaming mode
   - Check the console for any error messages

### Development

To modify or extend the UI:

1. Edit `src/cli/streamlit_ui.py`
2. The app will auto-reload when you save changes
3. Check the terminal for any error messages

## Architecture

The Streamlit UI integrates with:
- **LangGraph Agent**: Uses `src.tools.main.create_agent_graph()`
- **Laminar**: For observability and monitoring
- **Session State**: Maintains conversation history
- **Mermaid**: For graph visualization

## Next Steps

Potential improvements:
- Add conversation export functionality
- Implement conversation templates
- Add agent performance metrics
- Include tool usage statistics
- Add conversation search and filtering
