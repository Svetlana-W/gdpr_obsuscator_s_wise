# Makefile for a gdpr_obfuscator_s_wise project
# Author: Svetlana Wise

# Variables 
PROJECT_NAME := gdpr_obfuscator_s_wise  
PYTHON := python3 
WD := $(shell pwd)
PYTHONPATH := $(WD)/src
TESTS := $(WD)/tests
SHELL := /bin/bash
PIP := pip

# Default target, runs when you just type 'make' in the terminal
all: help

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	pytest

# Run the application 
run:
	@echo "Running the application..."
	$(PYTHON) src/core_obfuscator.py  
	@echo "Application finished running."
	
# Format code using black (optional)
format:
	@echo "Formatting code..."
	black src tests

# Lint code using flake8 (optional)
lint:
	@echo "Linting code..."
	flake8 src tests

# Clean up temporary files and build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache __pycache__ tests/__pycache__ src/__pycache__ dist build *.egg-info

# Generate documentation (optional - adapt to your documentation generator)
docs:
	@echo "Generating documentation..."
	sphinx-build -b html docs docs/_build

# Help target (displays available commands)
help:
	@echo "Available make commands:"
	@echo "  install    Install project dependencies"
	@echo "  test      Run tests"
	@echo "  run       Run the application"
	@echo "  format    Format code using black"
	@echo "  lint      Lint code using flake8"
	@echo "  clean     Clean up temporary files and build artifacts"
	@echo "  docs      Generate documentation"
	@echo "  help      Display this help message"
