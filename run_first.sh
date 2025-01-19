#/bin/bash

if [-d venv] or [-d .venv]; then
    echo "Virtual environment already exists"
else
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi