#!/bin/bash

# Get environment variables from the .env file
if [ ! -f ../.env ]; then
    echo "Environment file not found!"
    exit 1
fi
export $(cat ../.env | xargs)

# Path to Django project directory gets from the environment variable
PROJECT_DIR=$SERVER_PROJECT_ROOT

# Activate the virtual environment
VENV_DIR="$PROJECT_DIR/venv"  # Adjust this path if necessary
source "$VENV_DIR/bin/activate" || { echo "Failed to activate virtual environment!"; exit 1; }

# Add project directory to PYTHONPATH
export PYTHONPATH="$PROJECT_DIR"

# Navigate to the Django project directory
cd "$PROJECT_DIR/slopevision" || { echo "Project directory not found!"; exit 1; }

# Run the Django management command
python manage.py save_history

# Deactivate the virtual environment
deactivate

