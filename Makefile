# Makefile for a gdpr_obfuscator_s_wise project
# Author: Svetlana Wise

# Variables 
PROJECT_NAME := gdpr_obfuscator_s_wise  
PYTHON := python3 
WD := $(shell pwd)
PYTHONPATH := $(WD)/src
TESTS := $(WD)/tests
VENV := $(WD)/venv
VENV_PATH := $(VENV)/bin
SHELL := /bin/bash
PIP := $(VENV_PATH)/pip
PYTEST := $(VENV_PATH)/pytest

# Default target
all: help

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv venv
	@echo "Virtual environment created."

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test: venv
	@echo "Running tests..."
	$(PYTEST) tests
	@echo "Tests finished running."

# Run the application ** REPLACE with your actual values **
run: venv
	@echo "Running the application..." 
	$(VENV_PATH)/python src/cli.py config.json --output-bucket your-bucket-name --output-key output/data.csv 
	@echo "Application finished running."

# Format code using black
format: venv
	@echo "Formatting code..."
	black src tests

# Lint code using flake8
lint: venv
	@echo "Linting code..."
	flake8 src tests

# Clean up temporary files and build artifacts
clean: venv
	@echo "Cleaning up..."
	rm -rf .pytest_cache __pycache__ tests/__pycache__ src/__pycache__ dist build *.egg-info

# Generate documentation (optional - adapt to your documentation generator)
docs: venv
	@echo "Generating documentation..."
	sphinx-build -b html docs docs/_build

# Help target (displays available commands)
help: venv
	@echo "Available make commands:"
	@echo "  venv      Create virtual environment"
	@echo "  install   Install project dependencies"
	@echo "  test      Run tests"
	@echo "  run       Run the application"
	@echo "  format    Format code using black"
	@echo "  lint      Lint code using flake8"
	@echo "  clean     Clean up temporary files and build artifacts"
	@echo "  docs      Generate documentation"
	@echo "  help      Display this help message"