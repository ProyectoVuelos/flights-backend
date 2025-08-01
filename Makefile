.PHONY: help install run format test clean

.DEFAULT_GOAL := help

# A self-documenting makefile that reads the command descriptions from comments.
help:
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Install Python dependencies
	pip install -r requirements.txt

run: ## Run the main application
	python runner.py

format: ## Format code using black and isort
	black .
	isort .

test: ## Run tests with pytest
	pytest

clean: ## Remove temporary files and build artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf dist build
