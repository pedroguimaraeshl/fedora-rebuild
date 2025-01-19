#/bin/bash

echo "Running run_first.sh"

echo "Checking if virtual environment exists"
if [ -d venv ] || [ -d .venv ]; then
    echo "Enabling virtual environment"
    source venv/bin/activate
    echo "Sucess"
else
    python -m venv venv
    #sleep 3
    source venv/bin/activate
    #sleep 1
    pip install -r requirements.txt
fi
