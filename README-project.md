# DocPilot — Automatic Documentation Generator

## What it does
Upload a Python file and automatically generate
docstrings for every function using AI.

## Installation

1. Clone the repository
   git clone https://github.com/JuniorCesar-code/DocPilot.git

2. Go into the folder
   cd DocPilot

3. Install dependencies
   pip install fastapi uvicorn python-multipart anthropic python-dotenv

4. Create your .env file
   ANTHROPIC_API_KEY=your-key-here

5. Start the server
   py -m uvicorn main:app --reload

6. Open the frontend
   Open index.html in your browser

## How to use
1. Open index.html in your browser
2. Select a .py file
3. Choose documentation style (Google / NumPy / Sphinx)
4. Click Upload and analyse
5. Click any function to generate its docstring

## Project structure
main.py          → FastAPI backend (Person 1)
llm.py           → LLM integration (Person 2)
index.html       → Frontend (Person 3)
TEST_REPORT.md   → Test results
REQUIREMENTS.md  → Project requirements

## Team
Universität Duisburg-Essen
KI in Software Engineering — Sommersemester 2026
Prof. Dr. Dominik Sobania