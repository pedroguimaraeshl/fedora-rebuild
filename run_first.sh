#!/bin/bash

# Check if virtual environment exists (venv or .venv)
if [ -d venv ] || [ -d .venv ]; then
    echo "Enabling virtual environment..."
    source_cmd="venv/bin/activate"
    
    if ! [ -d "venv" ]; then
        source_cmd=".venv/bin/activate"
    fi
  
    source "$source_cmd"
    echo "Success!"

    # Check for the --install flag and install dependencies if present
    if [[ "$#" -gt 0 ]] && [[ "$1" == "--install" ]]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo "Dependencies installed."
    fi
else
    echo "No virtual environment found."
fi