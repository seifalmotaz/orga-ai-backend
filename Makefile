# Install development dependencies
install:
	uv sync

robyn:
	uv run robyn src/server/app.py --dev --host 0.0.0.0 --port 8080 --reload 

# Run the development server
server:
	@echo "Starting Robyn server..."
	uv run src/cli/runserver.py

# Run all tests
test:
	@echo "Running all tests..."
	pytest tests/ -v

# Run integration tests only
test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v

# Clean up temporary files
clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

makemigrations:
	uv run aerich migrate --name $(name)

migrate:
	uv run aerich upgrade