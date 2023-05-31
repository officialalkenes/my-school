# Makefile

# Variables
PYTHON := poetry run python
DJANGO := $(PYTHON) manage.py

# Default target
.DEFAULT_GOAL := help

# Install project dependencies
install:
	poetry install

# Run Django development server
server:
	$(DJANGO) runserver

# Create database tables
migrate:
	$(DJANGO) migrate

# Create a superuser
createsuperuser:
	$(DJANGO) createsuperuser

# Run Django tests
test:
	$(DJANGO) test

# Generate code coverage report
coverage:
	$(PYTHON) -m coverage run --source='.' manage.py test
	$(PYTHON) -m coverage report
	$(PYTHON) -m coverage html

# Clean up generated files
clean:
	$(PYTHON) -m coverage erase
	rm -rf htmlcov

# Show help message
help:
	@echo "Available targets:"
	@echo "  install           Install project dependencies"
	@echo "  runserver         Run Django development server"
	@echo "  migrate           Create database tables"
	@echo "  createsuperuser   Create a superuser"
	@echo "  test              Run Django tests"
	@echo "  coverage          Generate code coverage report"
	@echo "  clean             Clean up generated files"
	@echo "  help              Show this help message"

.PHONY: install runserver migrate createsuperuser test coverage clean help
