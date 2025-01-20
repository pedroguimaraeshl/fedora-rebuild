#/bin/bash

echo "Running run_first.sh"

echo "Checking if virtual environment exists"
if [ -d venv ] || [ -d .venv ]; then
    echo "Enabling virtual environment"
    source venv/bin/activate
    echo "Sucess"
else
    echo "Creating virtual environment"
    python -m venv venv

    echo "Activating virtual environment"
    source venv/bin/activate

    echo "Installing requirements"
    pip install -r requirements.txt
fi
