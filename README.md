# Orga-AI

An AI-powered organization and task management system built with LangGraph, FastAPI, and Streamlit.

## Features

- **🤖 LLM Agent**: Intelligent agent built with LangGraph for task management and organization
- **💬 Streamlit UI**: Interactive chat interface for communicating with the agent
- **🔄 Graph Visualization**: Real-time visualization of the agent's decision flow
- **📊 FastAPI Backend**: RESTful API for data management and integration
- **🗄️ Database**: Tortoise ORM with SQLite/PostgreSQL support

## Quick Start

### 1. Install Dependencies

```bash
# Install all dependencies
make install
```

### 2. Set Up Environment

Copy `.env.example` to `.env` and configure your API keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the Application

#### Option 1: Streamlit UI (Recommended for testing)
```bash
make streamlit
```
Open http://localhost:8501 in your browser.

#### Option 2: Command Line Interface
```bash
make runmodel
```

#### Option 3: FastAPI Server
```bash
make runserver
```
API available at http://localhost:8080

## Available Commands

```bash
make install      # Install dependencies
make streamlit    # Run Streamlit UI
make runmodel     # Run CLI chat interface
make runserver    # Run FastAPI server
make test         # Run tests
make clean        # Clean temporary files
```

## Project Structure

```
src/
├── cli/                 # Command-line interfaces
│   ├── runmodel.py     # CLI chat interface
│   ├── runserver.py    # FastAPI server launcher
│   └── streamlit_ui.py # Streamlit web interface
├── database/           # Database models and migrations
├── server/            # FastAPI application
└── tools/             # LangGraph agent and tools
```

## Documentation

- [Streamlit UI Guide](src/cli/README_STREAMLIT.md)
- [Task Management](TASKS.md)

## Development

This project uses:
- **Python 3.13+**
- **uv** for package management
- **LangGraph** for agent orchestration
- **Streamlit** for web UI
- **FastAPI** for API backend
- **Tortoise ORM** for database management