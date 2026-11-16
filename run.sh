#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file — please add your OPENAI_API_KEY and re-run."
    exit 1
fi

echo "Starting server at http://localhost:8000"
echo "Docs available at http://localhost:8000/docs"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
