FROM python:3.11-bookworm

WORKDIR /workspace

COPY . .

# Install uv and dependencies
RUN pip install uv
RUN uv sync

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "src.server.app:app", "--host", "0.0.0.0", "--port", "8080"]
