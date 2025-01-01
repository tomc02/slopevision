#!/bin/bash

# Check if the environment file exists at the first location
if [ ! -f ../.env ] && [ ! -f /slopevision/.env ]; then
    echo "Environment file not found!"
    exit 1
fi

# Use the first found .env file (prefer ../.env, fall back to /slopevision/.env)
if [ -f ../.env ]; then
    ENV_FILE="../.env"
else
    ENV_FILE="/slopevision/.env"
fi

# Path to Django project directory gets from the environment variable
PROJECT_DIR=$SERVER_PROJECT_ROOT

# Activate the virtual environment
VENV_DIR="$PROJECT_DIR/venv"  # Adjust this path if necessary
source "$VENV_DIR/bin/activate" || { echo "Failed to activate virtual environment!"; exit 1; }

# Add project directory to PYTHONPATH
export PYTHONPATH="$PROJECT_DIR"

# Navigate to the Django project directory
cd "$PROJECT_DIR/slopevision_django" || { echo "Project directory not found!"; exit 1; }

# Run the Django management command
python manage.py fetch_hzs_images

# Deactivate the virtual environment
deactivate

